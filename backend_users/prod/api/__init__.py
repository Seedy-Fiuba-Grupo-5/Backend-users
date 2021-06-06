from flask import Blueprint
from flask_restx import Api

# Namespaces
from .one_user_api import api as one_user_ns

api_bp = Blueprint('api', __name__)
api = Api(
    api_bp,
    title='Backend Users',
    version='1.0',
    description='Backend-users service operations'
)

api.add_namespace(one_user_ns)
