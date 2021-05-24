from flask import Blueprint
from flask_restful import Api, Resource
from prod.db_models.user_db_model import UserProjectDBModel

users_projects_list_api = Blueprint("users_projects_list_api", __name__)
api = Api(users_projects_list_api)


class UsersProjectsListResource(Resource):
    def get(self, user_id):
        projects_query =\
            UserProjectDBModel.query.filter(UserProjectDBModel.user_id ==
                                            user_id)
        if not projects_query:
            return 'The projects requested could not be found', 404
        response_object = \
            [user_project.serialize() for user_project in projects_query.all()]
        return response_object, 200


api.add_resource(UsersProjectsListResource, "/users/<user_id>/projects")
