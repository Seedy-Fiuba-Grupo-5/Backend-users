from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_restx import Namespace, Resource, fields
from prod.db_models.user_db_model import UserDBModel

REGISTER_FIELDS = ["token"]
ns = Namespace(
    'users/auth',
    description='One user authentication related operation'
)


@ns.route('')
@ns.param('user_id', 'The user identifier')
class AuthenticationResource(Resource):
    def get(self):
        data = request.get_json()
        if not self.check_values(data, REGISTER_FIELDS):
            return 'Missing values', 400
        token = data["token"]
        decoded = UserDBModel.decode_auth_token(token)
        requested_id = decoded["sub"]
        if UserDBModel.check_id(requested_id):
            return 'The token is valid', 200
        return 'The token is invalid', 400

    @staticmethod
    def check_values(json, fields_list):
        for value in fields_list:
            if value not in json:
                return False
        return True


api.add_resource(AuthenticationResource, "/users/auth")
