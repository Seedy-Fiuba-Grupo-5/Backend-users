from flask import Blueprint, request
from flask_restful import Api, Resource
from prod.db_models.user_db_model import UserDBModel

users_login_api = Blueprint("users_login_api", __name__)
api = Api(users_login_api)


class UsersLoginResource(Resource):
    def post(self):
        data = request.get_json()
        if not self.check_values(data, ["email", "password"]):
            return 'Faltan contraseña y/o password', 400
        email = data['email']
        password = data['password']
        id = UserDBModel.get_id(email,password)
        if id == -1:
            return 'Contraseña o e-mail incorrectos', 204
        response_object = {
            "email": email,
            "id": id
        }
        return response_object, 200

    @staticmethod
    def check_values(json, lista):
        for value in lista:
            if value not in json:
                return False
        return True


api.add_resource(UsersLoginResource, "/users/login")
