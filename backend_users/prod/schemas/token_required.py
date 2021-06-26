from flask_restx import Model, fields
from .constants import DESCRIPTIONS

token_required = Model('TokenRequired', {
    'token': fields.String(description=DESCRIPTIONS['token'],
                           required=True)
})
