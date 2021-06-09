from flask_restx import Namespace, Resource
from prod.db_models.user_db_model import UserDBModel
from flask import request


ns = Namespace(
    'users/auth',
    description='One user authentication related operation'
)


@ns.route('')
class AuthenticationResource(Resource):
    REGISTER_FIELDS = ["token"]

    def post(self):
        data = request.get_json()
        if not self.check_values(data, self.REGISTER_FIELDS):
            return 'Missing values', 401
        token = data["token"]
        token = bytes(token, encoding='utf8')
        decoded = UserDBModel.decode_auth_token(token)
        if UserDBModel.check_id(decoded):
            return 'The token is valid', 200
        return 'The token is invalid', 400

    @staticmethod
    def check_values(json, fields_list):
        for value in fields_list:
            if value not in json:
                return False
        return True
