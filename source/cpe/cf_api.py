import hashlib, json, random, requests, sys, time

from django.conf import settings
from cpe.cf_api_enums import *

weird_name = "39ce7"
x_user = ""
jsession = ""
weird_val  = ""
csrf_token = ""

user_agent = "Marat Yuldashev's Bot"




def is_gym(contest_id):
    return int(contest_id) >= 100000

def make_api_call(method_name, parameters):
    timestamp = int(time.time())
    rand = str(random.randrange(1000000)).zfill(6)
    parameters['time'] = timestamp
    parameters['apiKey'] = settings.CF_API_KEY
    
    parameters_string = "&".join(map(lambda p: str(p[0]) + "=" + str(p[1]), sorted(parameters.items())))
    string_to_hash = ("{rand}/{method_name}?{parameters}#{secret}"
                                    .format(rand = rand, method_name = method_name, parameters = parameters_string, secret = settings.CF_API_SECRET))

    hash = str(hashlib.sha512(string_to_hash.encode('utf-8')).hexdigest())
    
    address = "http://codeforces.ru/api/{method_name}?{parameters}&apiSig={rand}{hash}".format(
                                    method_name = method_name,
                                    parameters = parameters_string,
                                    rand = rand,
                                    hash = hash,
                                )
    
    response = requests.get(address)
    parsed_result = json.loads(response.text)
    return parsed_result['result']

def get_latest_submissions(contest_id):
    submissions = make_api_call("contest.status", { 
                                                    "contestId" : contest_id,
                                                    "from" : 1,
                                                    "count" : 1,
                                })
    return submissions

def parse_csrf_token(response):
    META_TAG = "<meta name=\"X-Csrf-Token\" content=\""
    i1 = response.text.find(META_TAG)
    if (i1 >= 0):
        i1 = i1 + len(META_TAG)
    
        global csrf_token
        csrf_token = response.text[i1:i1 + 32]    
    
def login_to_cf():
    print("Requesting CF homepage to update session cookies")
    make_cf_request_get("http://codeforces.com") # this is to make sure we have a valid session cookie

    print("Logging in to CF")
    response = make_cf_request_post("enter", {
                                                "action": "enter",
                                                "handle": settings.CPE_CF_HANDLE,
                                                "password": settings.CPE_CF_PASSWORD,
                                                "remember": "on",
                                             },
                                     False)
    global x_user
    x_user = response.cookies['X-User']
    
def restore_authentication_details(try_relogin = True):
    print("Restoring authentication details...")
    response = make_cf_request_get("http://codeforces.com/favourite/blogEntries")
    if response.status_code == 302 and try_relogin:
        login_to_cf()
        restore_authentication_details(False)
    else:    
        assert(response.status_code == 200)

def make_cf_request_get(url):
    global weird_val
    global jsession
    address = url
    response = requests.get(
                        address,
                        allow_redirects = False,
                        headers = {
                            "User-Agent": user_agent,
                        },
                        cookies = {
                            "X-User": x_user,
                            "JSESSIONID": jsession,
                            weird_name: weird_val, 
                        },
                    )

    if 'JSESSIONID' in response.cookies: jsession = response.cookies['JSESSIONID']
    if weird_name   in response.cookies: weird_val = response.cookies[weird_name]
    
    parse_csrf_token(response)
    return response
    
def make_cf_request_post(url_part, data = { }, try_relogin = True):
    address = "http://codeforces.com/" + url_part
    full_data = {
                    "csrf_token": csrf_token,
                    "lang": "en",
                }
    full_data.update(data)
        
    response = requests.post(
                        address,
                        allow_redirects = False,
                        data = full_data,
                        headers = {
                            "User-Agent": user_agent,
                        },
                        cookies={
                            "X-User": x_user,
                            "JSESSIONID": jsession,
                            weird_name: weird_val,
                        },
                    )
    
    if response.status_code == 403 and try_relogin:
        restore_authentication_details()
        return make_cf_request_post(url_part, data, False)
    
    return response

def submit_code(code, contest_id, problem_index, programming_language_code):
    address = "{contest_type}/{contest_id}/submit".format(contest_id = contest_id , contest_type = "gym" if is_gym(contest_id) else "contest")

    r = make_cf_request_post(address, data = {
                                "action": "submitSolutionFormSubmitted",
                                "submittedProblemIndex": problem_index,
                                "source": code,
                                "programTypeId": str(programming_language_code),
                            },
                        )
    if r.status_code != 302: raise Exception(str(r.status_code))

    latest_submissions = get_latest_submissions(contest_id)
    return latest_submissions[0]['id']
    
def get_judge_protocol(cf_submission_id):
    r = make_cf_request_post("data/judgeProtocol", data = {
                                                    "submissionId": str(cf_submission_id),
                                                })
                                                
    if r.status_code != 200: raise Exception(str(r.status_code))
    return json.loads(r.text)
    
def get_submission_verdict_details(cf_submission_id):
    r = make_cf_request_post("data/submitSource", data = {
                                                    "submissionId": str(cf_submission_id),
                                                })
                                                
    if r.status_code != 200: raise Exception(str(r.status_code))
    return json.loads(r.text)
    
def get_submission_verdict(cf_submission_id):
    verdict_details = get_submission_verdict_details(cf_submission_id)

    is_waiting = json.loads(verdict_details['waiting'])
    if is_waiting: return SUBMISSION_VERDICT.IN_PROGRESS

    compilation_failed = json.loads(verdict_details['compilationError'])
    if compilation_failed: return SUBMISSION_VERDICT.COMPILATION_ERROR
    
    last_test = verdict_details['testCount']
    last_verdict_key = "verdict#" + str(last_test)
    last_verdict = verdict_details[last_verdict_key]
    return SUBMISSION_VERDICT.parse(last_verdict)
        
def get_compilation_error(cf_submission_id):
    return get_judge_protocol(cf_submission_id)