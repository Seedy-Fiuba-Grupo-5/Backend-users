from flask_restx import Model, fields
from .constants import USER_BLOCKED

user_blocked = Model('ProjectNotFound', {
    'status': fields.String(example=USER_BLOCKED)
})
