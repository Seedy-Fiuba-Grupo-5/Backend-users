from flask import Blueprint  # , request
from flask_restful import Api, Resource
from prod.db_models.user_db_model import UserDBModel

one_user_api = Blueprint("one_user_api", __name__)
api = Api(one_user_api)


class UserResource(Resource):
    """def get(self,
            name_user):
        print(name_user)
        user = UserDBModel.query.filter(UserDBModel.name == name_user)
        if not user:
            return 'The user requested could not be found', 404
        response_object = user.serialize()
        return response_object, 200
    """

    def get(self, user_id):
        project_model = UserDBModel.query.get(user_id)
        if not project_model:
            return 'The project requested could not be found', 404
        response_object = project_model.serialize()
        return response_object, 200


api.add_resource(UserResource, "/users/<user_id>")
