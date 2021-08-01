from flask_restx import Model, fields
from .constants import MISSING_ARGS, DESCRIPTIONS

missing_args = Model('MissingArguments', {
    'status': fields.String(example=MISSING_ARGS),
    'missing_args': fields.List(fields.String()),
    'token': fields.String(description=DESCRIPTIONS['token'])
})
