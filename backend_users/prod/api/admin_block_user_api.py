from flask import request
from flask_restx import Namespace
from prod.api.base_resource import BaseResource
from prod.db_models.user_db_model import UserDBModel
from prod.db_models.admin_db_model import AdminDBModel
from prod.exceptions import BusinessError
from prod.schemas.constants import USER_NOT_FOUND_ERROR, REPEATED_EMAIL_ERROR
from prod.schemas.admin_representation import admin_representation
from prod.schemas.admin_block_code20 import admin_block_code20
from prod.schemas.user_email_repeated import user_email_repeated
from prod.schemas.user_login_not_found import user_login_not_found


ns = Namespace(
    'admins/users/<int:user_id>',
    description='Admin blocking user'
)


@ns.route('')
@ns.param('user_id', 'The user identifier')
class AdminResource(BaseResource):
    REQUIRED_VALUES = ['name', 'lastName', 'email', 'password', 'token']

    body_swg = ns.model(admin_representation.name, admin_representation)

    code_200_swg = ns.model(admin_block_code20.name, admin_block_code20)

    code_404_swg = ns.model(user_login_not_found.name, user_login_not_found)

    code_409_swg = ns.model(user_email_repeated.name, user_email_repeated)

    @ns.expect(body_swg)
    @ns.response(200, 'Success', code_200_swg)
    @ns.response(404, USER_NOT_FOUND_ERROR, code_404_swg)
    @ns.response(409, REPEATED_EMAIL_ERROR, code_409_swg)
    def patch(self, user_id):
        """Update user data"""
        try:
            user = AdminDBModel.query.get(user_id)
            if not user:
                ns.abort(404, status=USER_NOT_FOUND_ERROR)
            json = request.get_json()
            token_decoded = AdminDBModel.decode_auth_token(json['token'])
            if token_decoded != user_id:
                ns.abort(404, status=USER_NOT_FOUND_ERROR)
            UserDBModel.block(user_id)
            user = AdminDBModel.query.get(user_id)
            response_object = user.serialize()
            response_object['token'] = AdminDBModel.encode_auth_token(user_id)
            return response_object, 200
        except BusinessError as e:
            code, status = self.code_status[e.__class__]
            ns.abort(code, status=status)
        except KeyError:
            ns.abort(404, status=self.MISSING_VALUES_ERROR)