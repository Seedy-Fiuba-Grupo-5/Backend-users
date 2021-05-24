from flask import Blueprint
from flask_restful import Api, Resource
from prod.db_models.user_db_model import UserProjectDBModel

users_list_projects_api = Blueprint("users_list_projects_api", __name__)
api = Api(users_list_projects_api)


class UsersProjectListResource(Resource):
    @staticmethod
    def get(user_id):
        user = UserProjectDBModel.query.filter(UserProjectDBModel.user_id ==
                                               user_id)
        if not user:
            return 'The projects requested could not be found', 404
        response_object = \
            [user.serialize() for user in user.all()]
        return response_object, 200


api.add_resource(UsersProjectListResource, "/users/projects/<user_id>")
