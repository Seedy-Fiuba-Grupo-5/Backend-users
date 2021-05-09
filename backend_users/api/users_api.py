from flask import Blueprint  # , request
from flask_restful import Api, Resource
# from backend_users.db_models.user_db_model import UserDBModel

users_api = Blueprint("users_api", __name__)
api = Api(users_api)


class UsersResource(Resource):
    def get(self):
        response_object = [
            {
                "id": 1,
                "name": "Franco Martin",
                "last_name": "Di Maria",
                "email": "fdimaria@fi.uba.ar"
            }
        ]
        return response_object, 200


api.add_resource(UsersResource, "/users")
