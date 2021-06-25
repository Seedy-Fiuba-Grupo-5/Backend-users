from flask_restx import Namespace, fields
from prod.api.base_resource import BaseResource
from prod.db_models.user_db_model import UserDBModel
from flask import request


ns = Namespace(
    'users/auth',
    description='One user authentication related operation'
)


@ns.route('')
class AuthenticationResource(BaseResource):
    REGISTER_FIELDS = ["token"]
    VALID_TOKEN = 'valid_token'
    MISSING_ARGS_ERROR = 'missing_args'
    INVALID_TOKEN_ERROR = 'invalid_token'
    body_swg = ns.model('AuthenticationResourceInput', {
        'token': fields.String()
    })
    code_200_swg = ns.model('AuthenticationResourceOutput200', {
        "status": fields.String(example=VALID_TOKEN),
    })
    code_400_swg = ns.model('AuthenticationResourceOutput400', {
        'status': fields.String(example=MISSING_ARGS_ERROR)
    })
    code_401_swg = ns.model('AuthenticationResourceOutput401', {
        'status': fields.String(example=INVALID_TOKEN_ERROR)
    })

    @ns.expect(body_swg)
    @ns.response(200, 'Success', code_200_swg)
    @ns.response(400, 'Missing arguments', code_400_swg)
    @ns.response(401, 'The token is invalid', code_401_swg)
    def post(self):
        """Validate token"""
        data = request.get_json()
        missing_args = self.missing_values(data, self.REGISTER_FIELDS)
        if missing_args:
            response = {'status': self.MISSING_ARGS_ERROR}
            return response, 400
        token = data["token"]
        token = bytes(token, encoding='utf8')
        decoded = UserDBModel.decode_auth_token(token)
        if UserDBModel.check_id(decoded):
            response = {'status': self.VALID_TOKEN}
            return response, 200
        response = {'status': self.INVALID_TOKEN_ERROR}
        return response, 404
