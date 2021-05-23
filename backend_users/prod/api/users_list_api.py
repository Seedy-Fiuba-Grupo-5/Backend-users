from flask import Blueprint, request
from flask_restful import Api, Resource
from prod.db_models.user_db_model import UserDBModel

users_list_api = Blueprint("users_list_api", __name__)
api = Api(users_list_api)


class UsersListResource(Resource):
    def get(self):
        response_object =\
            [user.serialize() for user in UserDBModel.query.all()]
        return response_object, 200

    def post(self):
        json = request.get_json()
        if not self.check_values(json, ["email", "password"]):
            return 'insufficient information for User Login', 500
        email = request.get_json()['email']
        password = request.get_json()['password']
        if UserDBModel.get_id(email, password) == -1:
            return 'Contraseña o e-mail incorrectos', 204
        return UserDBModel.get_id(), 200

    @staticmethod
    def check_values(json, lista):
        for value in lista:
            if value not in json:
                return False
        return True


api.add_resource(UsersListResource, "/users")
