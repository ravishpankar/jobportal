from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


class JPLException(ValidationError):
    def JPLException(self, detail, code=None):
        self.detail = detail
        self.code = code

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response['status_code'] = response.status_code

    return response

SD_B_ED = 'Start date should be on or before enddate'
V_SD_B_LED = 'Start date should be on or after last enddate'
AMOUNTINVALID = 'Amount paid cannot be negative'
JOB_INVISIBLE = 'Job is invisible'
USER_ACCESS_DENY = "Invalid group and/or credentials"