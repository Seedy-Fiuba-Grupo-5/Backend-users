from flask import Blueprint, request
from flask_restful import Api, Resource
from prod.db_models.user_db_model import UserDBModel

users_list_api = Blueprint("users_list_api", __name__)
api = Api(users_list_api)

REGISTER_FIELDS = ("name", "lastName", "email", "password")
REPEATED_USER_ERROR = 'Ya existe un usuario registrado para el mail recibido'


class UsersListResource(Resource):
    def get(self):
        response_object =\
            [user.serialize() for user in UserDBModel.query.all()]
        return response_object, 200

    def post(self):
        data = request.get_json()
        if not self.check_values(data, REGISTER_FIELDS):
            return 'Parametros invalidos', 400
        name = data['name']
        lastName = data['lastName']
        email = data['email']
        password = data['password']
        id = UserDBModel.agregar_usuario(name,
                                         lastName,
                                         email,
                                         password)
        if id == -1:
            return REPEATED_USER_ERROR, 401
        response_object = {
            "name": name,
            "lastName": lastName,
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


api.add_resource(UsersListResource, "/users")
