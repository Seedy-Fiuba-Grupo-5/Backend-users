from flask import Blueprint
from flask_restx import Api

# Namespaces
from .one_user_api import ns as one_user_ns
from .users_list_api import ns as users_list_ns
from .users_login_api import ns as users_login_ns
from .users_projects_list_api import ns as users_projects_list_ns
from .auth_token_api import ns as auth_token_ns
from .admin_login_api import ns as admins_login_ns
from .one_admin_api import ns as one_admin_ns
from .admins_list_api import ns as admins_list_ns
from .projects_list_api import ns as projects_list_ns
from .admin_block_user_api import ns as admin_block_ns
from .metrics_api import ns as metrics_ns
from .one_seer_api import ns as one_seer_ns
from .messages_api import ns as messages_ns

NAMESPACES = (
    one_user_ns,
    users_list_ns,
    users_login_ns,
    users_projects_list_ns,
    auth_token_ns,
    admins_login_ns,
    one_seer_ns,
    one_admin_ns,
    admins_list_ns,
    projects_list_ns,
    admin_block_ns,
    metrics_ns,
    messages_ns
)

# Base Api
api_base_bp = Blueprint('api_base', __name__)
api_base = Api(
    api_base_bp,
    title='Backend Users: Api base',
    version='1.0',
    description='Backend-users service operations'
)

# Api v1
V1_URL = '/v1/'

api_v1_bp = Blueprint('api_v1', __name__, url_prefix=V1_URL)
api_v1 = Api(
    api_v1_bp,
    title='Backend Users: Api v1',
    version='1.0',
    description='Backend-users service operations'
)

# Add extensions
for ns in NAMESPACES:
    api_base.add_namespace(ns)
    api_v1.add_namespace(ns)
