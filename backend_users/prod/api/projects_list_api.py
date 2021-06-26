from flask_restx import Namespace
from flask import request
from prod.api.base_resource import BaseResource
from prod.db_models.user_db_model import UserProjectDBModel, UserDBModel
from prod.schemas.project_not_found import project_not_found
from prod.schemas.project_representation import project_representation
from prod.schemas.constants import DESCRIPTIONS, PROJECT_NOT_FOUND

ns = Namespace(
    'projects/<int:project_id>',
    description="User's projects related operations"
)


@ns.route('')
@ns.param('project_id', DESCRIPTIONS['project_id'])
class ProjectsListResource(BaseResource):
    code_200_sw = ns.model(project_representation.name, project_representation)
    code_404_sw = ns.model(project_not_found.name, project_not_found)

    @ns.response(200, 'Success', code_200_sw)
    @ns.response(404, PROJECT_NOT_FOUND, code_404_sw)
    def get(self, project_id):
        """Get project's data"""
        json = request.get_json()
        response_object = {}
        response_object['token'] = json['token']
        user_id = UserProjectDBModel.get_user_of_project_id(project_id)
        if user_id < 0:
            response_object['status'] = PROJECT_NOT_FOUND
            return response_object, 404
        response_object['project_id'] = project_id
        response_object['user_id'] = user_id
        return response_object, 200
