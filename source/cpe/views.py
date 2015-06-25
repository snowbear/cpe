import json, uuid
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe

from cpe.cf_api import *
from cpe.models import *
from cpe.cf_api_enums import *

def read_file(filename):
    with open (filename, "r") as file:
        data = file.read()
        return data

def read_exercise_data_file(exercise, filename):
    full_path = "{base_path}/exercise_data/{exercise_id}/{filename}".format(
                                                            base_path = settings.BASE_DIR,
                                                            exercise_id = exercise.id,
                                                            filename = filename,
                                                        )
    return read_file(full_path)
        
def read_template(extension, is_full_template, exercise):
    filename = "template.{extension}{suffix}".format(
                                                    extension = extension,
                                                    suffix = '.full' if is_full_template else '',
                                                    )

    return read_exercise_data_file(exercise, filename)

@login_required
def index(request):
    solved_exercises = set(Exercise.objects.filter(attempt__user = request.user, attempt__cf_verdict = SUBMISSION_VERDICT.AC).distinct())
    return render(request, 'cpe/index.html', {
        'exercises': Exercise.objects.all().order_by('id'),
        'solved': solved_exercises,
    })

@login_required
def solve(request, exercise_id, attempt_id = None):
    if attempt_id != None: attempt_id = int(attempt_id)
    attempt = Attempt.objects.get(pk = attempt_id) if attempt_id != None else None
    exercise = Exercise.objects.get(pk = exercise_id)
    template = read_template('cpp', False, exercise)
    (template_prefix , template_suffix) = template.split('USER_CODE', 1)
    return render(request, 'cpe/solve.html', {
                                            'task_description': mark_safe(read_exercise_data_file(exercise, 'description.html')),
                                            'template_prefix': template_prefix.rstrip('\n'),
                                            'template_suffix': template_suffix.lstrip('\n'),
                                            'exercise': exercise,
                                            'attempt_id': json.dumps(attempt_id),
                                            'current_code': attempt.code if attempt != None else "",
                                        })
    
@login_required
def submit(request, exercise_id):
    unique_id = str(uuid.uuid4())
    code = request.POST['code']
    exercise = Exercise.objects.get(pk = exercise_id)
    
    full_code_template = read_template('cpp', True, exercise)
    full_code = full_code_template.replace('UNIQUE_ID', unique_id).replace('USER_CODE', code)
    cf_submission_id = submit_code(full_code, exercise.cf_contest_id, exercise.cf_problem_index, 42)
    
    attempt = Attempt.objects.create(
                            user = request.user,
                            exercise = exercise,
                            unique_id = unique_id,
                            code = code,
                            cf_submission_id = cf_submission_id,
                            cf_verdict = SUBMISSION_VERDICT.IN_PROGRESS,
                        )
    
    # todo: make last parameter optional
    # return HttpResponseRedirect(reverse('cpe:solve', args = [ exercise.id ], submission_id = attempt.id ))
    return HttpResponseRedirect(reverse('cpe:solve2', args = [ exercise.id , attempt.id ] ))

verdict_code_mapping = {
    SUBMISSION_VERDICT.FAILED_TO_SUBMIT_TO_JUDGE: 'FL',
    SUBMISSION_VERDICT.IN_PROGRESS: 'IP',
    SUBMISSION_VERDICT.AC: 'AC',
    SUBMISSION_VERDICT.COMPILATION_ERROR: 'CE',
    SUBMISSION_VERDICT.WA: 'WA',
    SUBMISSION_VERDICT.TL: 'TL',
    SUBMISSION_VERDICT.ML: 'ML',
    SUBMISSION_VERDICT.RE: 'RE',
}

verdict_text_mapping = {
    SUBMISSION_VERDICT.FAILED_TO_SUBMIT_TO_JUDGE: 'Failed to judge',
    SUBMISSION_VERDICT.IN_PROGRESS: 'In progress',
    SUBMISSION_VERDICT.AC: 'Correct',
    SUBMISSION_VERDICT.COMPILATION_ERROR: 'Compilation error',
    SUBMISSION_VERDICT.WA: 'Wrong',
    SUBMISSION_VERDICT.TL: 'Time limit exceeded',
    SUBMISSION_VERDICT.ML: 'Memory limit exceeded',
    SUBMISSION_VERDICT.RE: 'Runtime error',
}
    
def get_verdict_text(attempt):
    return verdict_text_mapping[attempt.cf_verdict]

def status(request, submission_id):
    attempt = Attempt.objects.get(pk = submission_id)
    
    template_file = read_template('cpp', False, attempt.exercise)
    data = template_file.replace('USER_CODE', attempt.code)
    
    return render(request, 'cpe/status.html', {
                        'code' : data,
                        'status_text' : get_verdict_text(attempt),
                        'status_description' : attempt.cf_verdict_details,
                        
                        'attempt_id' : attempt.id,
                        'is_in_progress' : json.dumps(attempt.cf_verdict == SUBMISSION_VERDICT.IN_PROGRESS),
                    })

def get_update_status_result(submission_id):
    attempt = Attempt.objects.get(pk = submission_id)
    if attempt.cf_verdict == SUBMISSION_VERDICT.IN_PROGRESS:
        (current_status, tests_passed) = get_submission_verdict(attempt.cf_submission_id)
        if current_status != SUBMISSION_VERDICT.IN_PROGRESS:
            attempt.cf_verdict = current_status
            verdict_details = None
            if current_status == SUBMISSION_VERDICT.COMPILATION_ERROR:
                verdict_details = { 'compilation_error': get_compilation_error(attempt.cf_submission_id) }
            elif current_status == SUBMISSION_VERDICT.WA:
                submission_details = get_submission_verdict_details(attempt.cf_submission_id)
                failed_test = str(submission_details['testCount'])
                verdict_details = {
                                    'input': submission_details['input#' + failed_test],
                                    'output': submission_details['output#' + failed_test],
                                    'checker_comment': submission_details['checkerStdoutAndStderr#' + failed_test],
                                    'answer': submission_details['answer#' + failed_test],
                                }
            elif current_status != SUBMISSION_VERDICT.AC:
                submission_details = get_submission_verdict_details(attempt.cf_submission_id)
                failed_test = str(submission_details['testCount'])
                verdict_details = {
                                    'input': submission_details['input#' + failed_test],
                                    'answer': submission_details['answer#' + failed_test],
                                }
            attempt.cf_verdict_details = json.dumps(verdict_details)
            attempt.save()
    
    return attempt
                    
def update_status(request, submission_id):
    attempt = get_update_status_result(submission_id)
    return HttpResponse(json.dumps({
                                    'is_in_progress': attempt.cf_verdict == SUBMISSION_VERDICT.IN_PROGRESS,
                                    'verdict': verdict_text_mapping[attempt.cf_verdict],
                                    'verdict_code': verdict_code_mapping[attempt.cf_verdict],
                                    'verdict_details': json.loads(attempt.cf_verdict_details),
                                    }))
