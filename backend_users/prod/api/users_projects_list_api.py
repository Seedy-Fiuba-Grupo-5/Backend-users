from flask import Blueprint, request
from flask_restful import Api, Resource
from prod.db_models.user_db_model import UserProjectDBModel

users_projects_list_api = Blueprint("users_projects_list_api", __name__)
api = Api(users_projects_list_api)


class UsersProjectsListResource(Resource):
    def get(self, user_id):
        id_projects_list =\
            UserProjectDBModel.get_projects_of_user_id(user_id)
        response_object = {
            "user_id": int(user_id),
            "project_id": id_projects_list
        }
        return response_object, 200

    def post(self, user_id):
        data = request.get_json()
        user_id = int(user_id)
        project_id = data['project_id']
        id_projects_list =\
            UserProjectDBModel.add_project_to_user_id(user_id, project_id)
        response_object = {
            "user_id": user_id,
            "project_id": id_projects_list
        }
        return response_object, 201


api.add_resource(UsersProjectsListResource, "/users/<user_id>/projects")
