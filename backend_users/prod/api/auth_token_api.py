from flask_restx import Namespace
from flask import request
from prod.api.base_resource import BaseResource
from prod.db_models.user_db_model import UserDBModel
from prod.schemas.valid_token import valid_token
from prod.schemas.invalid_token import invalid_token
from prod.schemas.missing_args import missing_args
from prod.schemas.token_representation import token_representation
from prod.schemas.constants import MISSING_ARGS, VALID_TOKEN, INVALID_TOKEN,\
    USER_NOT_FOUND


ns = Namespace(
    'users/auth',
    description='One user authentication related operation'
)


@ns.route('')
class AuthenticationResource(BaseResource):
    REGISTER_FIELDS = ["token", "user_id"]

    body_swg = ns.model(token_representation.name, token_representation)
    code_200_swg = ns.model(valid_token.name, valid_token)
    code_400_swg = ns.model(missing_args.name, missing_args)
    code_401_swg = ns.model(invalid_token.name, invalid_token)

    @ns.expect(body_swg)
    @ns.response(200, 'Success', code_200_swg)
    @ns.response(400, MISSING_ARGS, code_400_swg)
    @ns.response(401, INVALID_TOKEN, code_401_swg)
    def post(self):
        """Validate token"""
        data = request.get_json()
        missing_args = self.missing_values(data, self.REGISTER_FIELDS)
        if missing_args:
            response = {'status': MISSING_ARGS}
            return response, 400
        token = data["token"]
        token = bytes(token, encoding='utf8')
        decoded = UserDBModel.decode_auth_token(token)
        if decoded != data['user_id']:
            response = {'status': INVALID_TOKEN}
            return response, 401
        if UserDBModel.check_id(decoded):
            encoded = UserDBModel.encode_auth_token(decoded)
            response = {'status': VALID_TOKEN, 'token': encoded}
            return response, 200
        response = {'status': USER_NOT_FOUND}
        return response, 401
