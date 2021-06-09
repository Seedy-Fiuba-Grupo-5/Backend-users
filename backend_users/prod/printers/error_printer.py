from prod.exceptions.repeated_email_error import RepeatedEmailError
REPEATED_EMAIL_ERROR = 'repeated_email'


class ErrorPrinter:
    code_status = {
        RepeatedEmailError: (409, 'repeated_email')
    }

    @classmethod
    def print(cls, business_error):
        return cls.code_status[business_error.__class__]
