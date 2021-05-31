from flask import Blueprint, request
from flask_restful import Api, Resource
from prod import db
from prod.db_models.user_db_model import UserProjectDBModel

users_projects_list_api = Blueprint("users_projects_list_api", __name__)
api = Api(users_projects_list_api)


class UsersProjectsListResource(Resource):
    def get(self, user_id):
        projects_query =\
                UserProjectDBModel.get_projects_associated_to_user_id(user_id)
        response_object = \
            [user_project.serialize() for user_project in projects_query.all()]
        return response_object, 200

    def post(self, user_id):
        data = request.get_json()
        project_id = data['project_id']
        user_model = UserProjectDBModel(user_id=user_id, project_id=project_id)
        db.session.add(user_model)
        db.session.commit()
        db.session.refresh(user_model)
        response_object = user_model.serialize()
        return response_object, 201


api.add_resource(UsersProjectsListResource, "/users/<user_id>/projects")
