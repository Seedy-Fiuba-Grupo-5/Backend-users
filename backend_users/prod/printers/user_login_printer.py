from prod.exceptions import UserNotFoundError, WrongPasswordError

class UserLoginPrinter:
    code_status = {
        UserNotFoundError: (404, 'user_not_found'),
        WrongPasswordError: (401, 'wrong_password')
    }

    @classmethod
    def print_error(cls, business_error):
        return cls.code_status[business_error.__class__]
