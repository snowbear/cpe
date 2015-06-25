from django.contrib.auth.models import User
from django.db import models

class Exercise(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    cf_contest_id = models.IntegerField()
    cf_problem_index = models.CharField(max_length = 3)

class Attempt(models.Model):
    user = models.ForeignKey(User, null = False)
    exercise = models.ForeignKey(Exercise, null = False)
    unique_id = models.CharField(max_length = 40, unique = True)
    code = models.CharField(max_length = 2000)
    cf_submission_id = models.IntegerField()
    cf_verdict = models.IntegerField()
    cf_verdict_details = models.CharField(max_length = 1000)
