from flask_restx import Model, fields
from prod.schemas.constants import MISSING_VALUES_ERROR

user_repeated = Model('MissingArguments', {
    'status': fields.String(example=MISSING_VALUES_ERROR),
    'missing_args': fields.List(fields.String())
})
