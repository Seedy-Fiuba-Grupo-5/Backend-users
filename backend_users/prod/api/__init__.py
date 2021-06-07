from flask import Blueprint
from flask_restx import Api

# Namespaces
from .one_user_api import ns as one_user_ns
from .users_list_api import ns as users_list_ns
from .users_login_api import ns as users_login_ns
from .users_projects_list_api import ns as users_projects_list_ns

# Base Api

api_base_bp = Blueprint('api_base', __name__)
api_base = Api(
    api_base_bp,
    title='Backend Users: Api base',
    version='1.0',
    description='Backend-users service operations'
)

api_base.add_namespace(one_user_ns)
api_base.add_namespace(users_list_ns)
api_base.add_namespace(users_login_ns)
api_base.add_namespace(users_projects_list_ns)

# Api v1

V1_URL = '/v1/'

api_v1_bp = Blueprint('api_v1', __name__, url_prefix=V1_URL)
api_v1 = Api(
    api_v1_bp,
    title='Backend Users: Api v1',
    version='1.0',
    description='Backend-users service operations'
)

api_v1.add_namespace(one_user_ns)
api_v1.add_namespace(users_list_ns)
api_v1.add_namespace(users_login_ns)
api_v1.add_namespace(users_projects_list_ns)
