from flask_restx import Model, fields
from prod.schemas.constants import INVALID_SEER_ID

user_email_repeated = Model('UserEmailRepeated', {
    'user_id': fields.String(example=INVALID_SEER_ID)
})
