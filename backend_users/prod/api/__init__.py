from flask import Blueprint
from flask_restx import Api

# Namespaces
from .one_user_api import ns as one_user_ns
from .users_list_api import ns as users_list_ns
from .users_login_api import ns as users_login_ns

api_bp = Blueprint('api', __name__)
api = Api(
    api_bp,
    title='Backend Users',
    version='1.0',
    description='Backend-users service operations'
)

api.add_namespace(one_user_ns)
api.add_namespace(users_list_ns)
api.add_namespace(users_login_ns)
