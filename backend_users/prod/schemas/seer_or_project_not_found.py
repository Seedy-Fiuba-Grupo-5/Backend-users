from flask_restx import Model, fields
from prod.schemas.constants import USER_NOT_FOUND_ERROR
from prod.schemas.constants import PROJECT_NOT_FOUND

user_email_repeated = Model('UserEmailRepeated', {
    'user_id': fields.String(example=USER_NOT_FOUND_ERROR),
    'project_id': fields.String(example=PROJECT_NOT_FOUND)
})
