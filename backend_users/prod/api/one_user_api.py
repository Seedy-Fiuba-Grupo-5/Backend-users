from flask import request
from flask_restx import Namespace
from prod.api.base_resource import BaseResource
from prod.db_models.user_db_model import UserDBModel
from prod.exceptions import BusinessError, RepeatedEmailError, UserBlockedError
from prod.schemas.user_code20 import user_code20
from prod.schemas.admin_representation import admin_representation
from prod.schemas.user_login_not_found import user_login_not_found
from prod.schemas.user_email_repeated import user_email_repeated
from prod.schemas.constants import USER_NOT_FOUND_ERROR, REPEATED_EMAIL_ERROR,\
    MISSING_VALUES_ERROR, USER_BLOCKED
from prod.schemas.patch_user import patch_user

ns = Namespace(
    'users/<int:user_id>',
    description='One user related operations'
)


@ns.route('')
@ns.param('user_id', 'The user identifier')
class UserResource(BaseResource):

    code_status = {
        RepeatedEmailError: (409, 'repeated_email'),
        UserBlockedError: (406, 'user_blocked')
    }

    body_swg = ns.model(admin_representation.name, admin_representation)

    patch_swg = ns.model(patch_user.name, patch_user)

    code_200_swg = ns.model(user_code20.name, user_code20)

    code_404_swg = ns.model(user_login_not_found.name, user_login_not_found)

    code_409_swg = ns.model(user_email_repeated.name, user_email_repeated)

    @ns.response(200, 'Success', code_200_swg)
    @ns.response(404, USER_NOT_FOUND_ERROR, code_404_swg)
    def get(self, user_id):
        """Get user data"""
        user = UserDBModel.query.get(user_id)
        if not user:
            ns.abort(404, status=USER_NOT_FOUND_ERROR)
        response_object = user.serialize()
        return response_object, 200

    @ns.expect(patch_swg)
    @ns.response(200, 'Success', code_200_swg)
    @ns.response(404, USER_NOT_FOUND_ERROR, patch_user)
    @ns.response(409, REPEATED_EMAIL_ERROR, code_409_swg)
    def patch(self, user_id):
        """Update user data"""
        try:
            user = UserDBModel.query.get(user_id)
            if not user:
                ns.abort(404, status=USER_NOT_FOUND_ERROR)
            json = request.get_json()
            token_decoded = UserDBModel.decode_auth_token(json['token'])
            if token_decoded != user_id:
                ns.abort(404, status=USER_NOT_FOUND_ERROR)
            if UserDBModel.get_active_status(user_id) is False:
                ns.abort(401,
                         status=USER_BLOCKED)
            user.update(
                name=json.get('name', user.name),
                lastName=json.get('lastName', user.lastName),
                email=json.get('email', user.email),
                password=json.get('password', user.password),
                seer=json.get('seer', user.seer),
                expo_token=json.get('expo_token', user.expo_token)
            )
            user = UserDBModel.query.get(user_id)
            response_object = user.serialize()
            response_object['token'] = UserDBModel.encode_auth_token(user_id)
            return response_object, 200
        except BusinessError as e:
            code, status = self.code_status[e.__class__]
            ns.abort(code, status=status)
        except KeyError:
            ns.abort(404, status=MISSING_VALUES_ERROR)
