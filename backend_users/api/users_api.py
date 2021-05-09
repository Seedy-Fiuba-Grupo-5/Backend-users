from flask import Blueprint  # , request
from flask_restful import Api, Resource
from backend_users.db_models.user_db_model import UserDBModel

users_api = Blueprint("users_api", __name__)
api = Api(users_api)


class UsersResource(Resource):
    def get(self):
        response_object = {}
        response_object =\
            [user.serialize() for user in UserDBModel.query.all()]
        return response_object, 200


api.add_resource(UsersResource, "/users")
