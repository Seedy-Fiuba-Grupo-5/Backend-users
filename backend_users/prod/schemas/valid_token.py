from flask_restx import Model, fields
from .constants import VALID_TOKEN

valid_token = Model('ValidToken', {
    'status': fields.String(example=VALID_TOKEN)
})
