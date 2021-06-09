from flask_restx import Namespace, Resource, fields
from prod.db_models.user_db_model import UserDBModel
from flask import request


ns = Namespace(
    'users/auth',
    description='One user authentication related operation'
)


@ns.route('')
class AuthenticationResource(Resource):
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

    @ns.marshal_with(code_200_swg, code=200)
    @ns.response(400, 'Missing values', code_400_swg)
    @ns.response(401, 'The token is invalid', code_401_swg)
    def post(self):
        data = request.get_json()
        if not self.check_values(data, self.REGISTER_FIELDS):
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

    @staticmethod
    def check_values(json, fields_list):
        for value in fields_list:
            if value not in json:
                return False
        return True
