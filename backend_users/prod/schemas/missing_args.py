from flask_restx import Model, fields
from .constants import MISSING_ARGS

missing_args = Model('MissingArguments', {
    'status': fields.String(example=MISSING_ARGS)
})
