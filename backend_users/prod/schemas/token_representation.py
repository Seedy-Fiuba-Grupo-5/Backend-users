from flask_restx import Model, fields
from .constants import DESCRIPTIONS

token_representation = Model('TokenRepresentation', {
    'token': fields.String(example=DESCRIPTIONS['token'])
})
