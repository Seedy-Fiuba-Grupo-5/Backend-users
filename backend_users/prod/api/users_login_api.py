from flask_restx import Namespace, fields
from flask import request
from prod.api.base_resource import BaseResource
from prod.db_models.user_db_model import UserDBModel
from prod.exceptions import BusinessError, UserNotFoundError, \
    WrongPasswordError
from prod.schemas.constants import WRONG_PASS_ERROR, MISSING_ARGS_ERROR, \
    USER_NOT_FOUND_ERROR
from prod.schemas.user_login import user_login
from prod.schemas.user_email_repeated import user_email_repeated
from prod.schemas.user_login_code20 import user_login_code20
from prod.schemas.user_login_not_found import user_login_not_found


ns = Namespace(
    'users/login',
    description='Users login operations'
)


@ns.route('')
class UsersLoginResource(BaseResource):
    REQUIRED_VALUES = ['email', 'password']

    code_status = {
        UserNotFoundError: (404, USER_NOT_FOUND_ERROR),
        WrongPasswordError: (401, WRONG_PASS_ERROR)
    }
    body_swg = ns.model(user_login.name, user_login)

    code_200_swg = ns.model(user_login_code20.name, user_login_code20)

    code_400_swg = ns.model('LoginOutput400', {
        'status': fields.String(example=MISSING_ARGS_ERROR),
        'missing_args': fields.List(fields.String())
    })

    code_401_swg = ns.model(user_email_repeated.name, user_email_repeated)

    code_404_swg = ns.model(user_login_not_found.name, user_login_not_found)

    @ns.expect(body_swg)
    @ns.response(200, 'Success', code_200_swg)
    @ns.response(400, 'Missing arguments', code_400_swg)
    @ns.response(401, 'Wrong password', code_401_swg)
    @ns.response(404, 'User not found', code_404_swg)
    def post(self):
        """Login"""
        try:
            data = request.get_json()
            missing_args = self.missing_values(data, self.REQUIRED_VALUES)
            if missing_args:
                ns.abort(400, status=MISSING_ARGS_ERROR,
                         missing_args=missing_args)
            id = UserDBModel.get_id(data['email'], data['password'])
            token = UserDBModel.encode_auth_token(id)
            response_object = {
                "email": data['email'], "id": id, "token": token}
            return response_object, 200
        except BusinessError as e:
            code, status = self.code_status[e.__class__]
            ns.abort(code, status=status)
