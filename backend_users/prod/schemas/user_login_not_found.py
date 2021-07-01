from flask_restx import Model, fields
from .constants import USER_NOT_FOUND_ERROR

user_login_not_found = Model('UserNotFound', {
    'status': fields.String(example=USER_NOT_FOUND_ERROR)
})
