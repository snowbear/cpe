from enum import IntEnum

class SUBMISSION_VERDICT(IntEnum):
    FAILED_TO_SUBMIT_TO_JUDGE = -1
    IN_PROGRESS = 0
    COMPILATION_ERROR = 2
    WA = 10
    TL = 11
    ML = 12
    RE = 13

    OTHER = 90
    AC = 100
    
    def parse(str):
        return text_mapping[str]
        
text_mapping = {
            "WRONG_ANSWER": SUBMISSION_VERDICT.WA,
            "RUNTIME_ERROR": SUBMISSION_VERDICT.RE,
            "TIME_LIMIT_EXCEEDED": SUBMISSION_VERDICT.TL,
            "MEMORY_LIMIT_EXCEEDED": SUBMISSION_VERDICT.ML,
            "OK": SUBMISSION_VERDICT.AC,
        }
