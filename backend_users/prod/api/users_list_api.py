from flask import Blueprint, request
from flask_restful import Api, Resource
from prod.db_models.user_db_model import UserDBModel

users_list_api = Blueprint("users_list_api", __name__)
api = Api(users_list_api)

REGISTER_FIELDS = ("name", "lastName", "email", "password")
REPEATED_USER_ERROR = 'User already registered'


class UsersListResource(Resource):
    def get(self):
        response_object =\
            [user.serialize() for user in UserDBModel.query.all()]
        return response_object, 200

    def post(self):
        data = request.get_json()
        if not self.check_values(data, REGISTER_FIELDS):
            return 'Missing values', 400
        name = data['name']
        lastname = data['lastName']
        email = data['email']
        password = data['password']
        requested_id = UserDBModel.add_user(name,
                                            lastname,
                                            email,
                                            password)
        if requested_id == -1:
            return REPEATED_USER_ERROR, 401
        response_object = {
            "name": name,
            "lastName": lastname,
            "email": email,
            "id": requested_id
        }
        return response_object, 201

    @staticmethod
    def check_values(json, fields_list):
        for value in fields_list:
            if value not in json:
                return False
        return True


api.add_resource(UsersListResource, "/users")
