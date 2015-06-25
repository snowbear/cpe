from django.test import TestCase
from cpe.cf_api import *
from cpe.cf_api_enums import *

class cf_api_test(TestCase):
    def test_get_submission_verdict(self):
        testcases = [ 
                ( 11633843 , SUBMISSION_VERDICT.AC),
                ( 11089031 , SUBMISSION_VERDICT.COMPILATION_ERROR),
                ( 11088538 , SUBMISSION_VERDICT.WA),
                ( 11657239 , SUBMISSION_VERDICT.RE),
                ( 11044437 , SUBMISSION_VERDICT.TL),
                ( 11698594 , SUBMISSION_VERDICT.ML),
                ( 11480282 , SUBMISSION_VERDICT.IN_PROGRESS),
               ]
        
        for (cf_submission_id, expected_verdict) in testcases:
            actual_verdict = get_submission_verdict(cf_submission_id)
            self.assertEqual(actual_verdict, expected_verdict, "Submission id -  " + str(cf_submission_id))