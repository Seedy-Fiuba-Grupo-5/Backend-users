from flask_restx import Model, fields
from .constants import INVALID_TOKEN

invalid_token = Model('InvalidToken', {
    'status': fields.String(example=INVALID_TOKEN)
})
