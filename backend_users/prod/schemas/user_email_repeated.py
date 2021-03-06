from flask_restx import Model, fields
from prod.schemas.constants import REPEATED_EMAIL_ERROR

user_email_repeated = Model('UserEmailRepeated', {
    'status': fields.String(example=REPEATED_EMAIL_ERROR)
})
