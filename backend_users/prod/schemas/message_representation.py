from flask_restx import Model, fields
from .constants import DESCRIPTIONS

message_representation = Model('MessageRepresentation', {
    'user_id': fields.Integer(description=DESCRIPTIONS['user_id']),
    'token': fields.String(description=DESCRIPTIONS['token']),
})
