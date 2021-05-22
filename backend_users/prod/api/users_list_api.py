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
        email = request.get_json()['email']
        password = request.get_json()['password']
        if not UserDBModel.comprobar_relacion_usuario_pass(email,
                                                           password):
            return 'Contraseña o e-mail incorrectos', 204
        return UserDBModel.get_id(), 200

api.add_resource(UsersListResource, "/users")
