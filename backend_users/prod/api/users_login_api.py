from flask import Blueprint
from flask_restful import Api, Resource
from prod.db_models.user_db_model import UserDBModel

users_login_api = Blueprint("users_login_api", __name__)
api = Api(users_login_api)


class UsersLoginResource(Resource):

    @staticmethod
    def post(self):
        user = UserDBModel.query.get(user_id)
        if not user:
            return 'Contraseña o e-mail incorrectos', 204
        response_object = user.serialize()
        return response_object, 200


api.add_resource(UsersLoginResource, "/users/login")
