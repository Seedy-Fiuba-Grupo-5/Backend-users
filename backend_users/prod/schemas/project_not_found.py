from flask_restx import Model, fields
from .constants import PROJECT_NOT_FOUND

project_not_found = Model('ProjectNotFound', {
    'status': fields.String(example=PROJECT_NOT_FOUND)
})
