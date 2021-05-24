from flask import Blueprint
from flask_restful import Api, Resource
from prod.db_models.user_db_model import UserDBModel

one_user_api = Blueprint("one_user_api", __name__)
api = Api(one_user_api)


class UserResource(Resource):
    @staticmethod
    def get(user_id):
        user = UserDBModel.query.get(user_id)
        if not user:
            return 'Email or password incorrect', 204
        response_object = user.serialize()
        return response_object, 200


api.add_resource(UserResource, "/users/<user_id>")
