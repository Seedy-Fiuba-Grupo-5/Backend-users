from flask_restx import Namespace, fields
from flask import request
from prod.db_models.user_db_model import UserDBModel
from prod.api.base_resource import BaseResource
from prod.db_models.user_project_db_model import UserProjectDBModel
from prod.exceptions import UserNotFoundError, \
    WrongPasswordError, UserBlockedError
from prod.schemas.constants import WRONG_PASS_ERROR, MISSING_ARGS_ERROR, \
    USER_NOT_FOUND_ERROR, USER_BLOCKED
from prod.schemas.user_login_code20 import user_login_code20
from prod.schemas.user_login_not_found import user_login_not_found
from prod.schemas.user_blocked import user_blocked

ns = Namespace(
    'users/<int:user_id>/projects',
    description="User's projects related operations"
)


@ns.route('')
@ns.param('user_id', 'The user identifier')
class UsersProjectsListResource(BaseResource):
    code_status = {
        UserNotFoundError: (404, USER_NOT_FOUND_ERROR),
        WrongPasswordError: (401, WRONG_PASS_ERROR),
        UserBlockedError: (403, USER_BLOCKED)
    }

    code_401_swg = ns.model(user_blocked.name, user_blocked)

    code_200_swg = ns.model(user_login_code20.name, user_login_code20)

    code_400_swg = ns.model('LoginOutput400', {
        'status': fields.String(example=MISSING_ARGS_ERROR),
        'missing_args': fields.List(fields.String())
    })

    code_404_swg = ns.model(user_login_not_found.name, user_login_not_found)

    body_swg = ns.model('User projects input', {
        'project_id': fields.Integer(
            required=True, description='The project id'),
    })

    code_20x_swg = ns.model('User projects input 20x', {
        'user_id': fields.Integer(description='The user id'),
        'project_id': fields.List(
            fields.Integer(description='One of the user projects id')
        )
    })

    @ns.response(200, 'Success', code_20x_swg)
    def get(self, user_id):
        """Get user's projects"""
        id_projects_list = \
            UserProjectDBModel.get_projects_of_user_id(user_id)
        response_object = {
            "user_id": user_id,
            "project_id": id_projects_list
        }
        return response_object, 200

    @ns.expect(body_swg)
    @ns.response(201, 'Success', code_20x_swg)
    @ns.response(404, 'User not found', code_404_swg)
    def post(self, user_id):
        """Add project to user"""
        data = request.get_json()
        if UserDBModel.check_id(user_id) != 1:
            ns.abort(404,
                     status=USER_NOT_FOUND_ERROR)
        id_projects_list = UserProjectDBModel.add_project_to_user_id(
            user_id, data['project_id'])
        response_object = {
            "user_id": user_id,
            "project_id": id_projects_list
        }
        return response_object, 201
