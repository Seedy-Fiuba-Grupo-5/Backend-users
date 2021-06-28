from flask import request
from flask_restx import Namespace
from prod.api.base_resource import BaseResource
from prod.db_models.user_db_model import UserDBModel
from prod.exceptions import BusinessError
from prod.schemas.constants import USER_NOT_FOUND_ERROR
from prod.schemas.admin_block_representation import admin_block_representation
from prod.schemas.admin_block_code20 import admin_block_code20
from prod.schemas.user_login_not_found import user_login_not_found
from prod.schemas.constants import MISSING_VALUES_ERROR

ns = Namespace(
    'admins/users/<int:user_id>',
    description='Admin blocking user'
)


@ns.route('')
@ns.param('user_id', 'The user identifier')
class AdminResource(BaseResource):
    REQUIRED_VALUES = ['token', "id_admin"]

    body_swg = ns.model(admin_block_representation.name,
                        admin_block_representation)

    code_200_swg = ns.model(admin_block_code20.name, admin_block_code20)

    code_404_swg = ns.model(user_login_not_found.name, user_login_not_found)

    @ns.expect(body_swg)
    @ns.response(200, 'Success', code_200_swg)
    @ns.response(404, USER_NOT_FOUND_ERROR, code_404_swg)
    def patch(self, user_id):
        """Update user data, blocking user"""
        try:
            user = UserDBModel.query.get(user_id)
            if not user:
                ns.abort(404, status=USER_NOT_FOUND_ERROR)
            json = request.get_json()
            token_decoded = UserDBModel.decode_auth_token(json['token'])
            id_admin = json['id_admin']
            if token_decoded != id_admin:
                ns.abort(404, status=USER_NOT_FOUND_ERROR)
            UserDBModel.block_and_unblock(user_id)
            user = UserDBModel.query.get(user_id)
            response_object = user.serialize()
            response_object['token'] = UserDBModel.encode_auth_token(user_id)
            return response_object, 200
        except BusinessError as e:
            code, status = self.code_status[e.__class__]
            ns.abort(code, status=status)
        except KeyError:
            ns.abort(404, status=MISSING_VALUES_ERROR)
