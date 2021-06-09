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
    code_200_swg = ns.model('AuthenticationResource output 200', {
        "status": fields.String(description='The token is valid'),
    })
    code_400_swg = ns.model('AuthenticationResource output 400', {
        'status': fields.String(description='Missing values')
    })
    code_401_swg = ns.model('AuthenticationResource output 401', {
        'status': fields.String(description='The token is invalid')
    })

    @ns.response(200, 'Success', code_200_swg)
    @ns.response(400, 'Missing arguments', code_400_swg)
    @ns.response(401, 'The token is invalid', code_401_swg)
    def post(self):
        data = request.get_json()
        missing_args = self.missing_values(data, self.REGISTER_FIELDS)
        if missing_args != []:
            response = {'status': 'Missing values'}
            return response, 400
        token = data["token"]
        token = bytes(token, encoding='utf8')
        decoded = UserDBModel.decode_auth_token(token)
        if UserDBModel.check_id(decoded):
            response = {'status': 'The token is valid'}
            return response, 200
        response = {'status': 'The token is invalid'}
        return response, 404
