from flask_restx import Model, fields
from .constants import DESCRIPTIONS

project_representation = Model('ProjectRepresentation', {
    'project_id': fields.Integer(description=DESCRIPTIONS['project_id']),
    'user_id': fields.Integer(description=DESCRIPTIONS['user_id']),
    'token': fields.String(description=DESCRIPTIONS['token']),
})
