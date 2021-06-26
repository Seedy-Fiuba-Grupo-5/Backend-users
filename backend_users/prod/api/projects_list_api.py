from flask_restx import Namespace
from flask import request
from prod.api.base_resource import BaseResource
from prod.db_models.user_db_model import UserProjectDBModel, UserDBModel
from prod.schemas.project_not_found import project_not_found
from prod.schemas.project_representation import project_representation
from prod.schemas.token_required import token_required
from prod.schemas.missing_args import missing_args
from prod.schemas.constants import DESCRIPTIONS, PROJECT_NOT_FOUND,\
    MISSING_ARGS

ns = Namespace(
    'projects/<int:project_id>',
    description="User's projects related operations"
)


@ns.route('')
@ns.param('project_id', DESCRIPTIONS['project_id'])
class ProjectsListResource(BaseResource):
    REQ_FIELDS = ['token']

    body_swg = ns.model(token_required.name, token_required)
    code_200_swg = ns.model(project_representation.name,
                            project_representation)
    code_400_swg = ns.model(missing_args.name, missing_args)
    code_404_swg = ns.model(project_not_found.name, project_not_found)

    @ns.expect(body_swg)
    @ns.response(200, 'Success', code_200_swg)
    @ns.response(400, MISSING_ARGS, code_400_swg)
    @ns.response(404, PROJECT_NOT_FOUND, code_404_swg)
    def get(self, project_id):
        """Get project's data"""
        response_object = {}
        data = request.get_json()
        missing_args = self.missing_values(data, self.REQ_FIELDS)
        if missing_args:
            response_object['status'] = MISSING_ARGS
            response_object['missing_args'] = missing_args
            return response_object, 400
        user_id = UserProjectDBModel.get_user_of_project_id(project_id)
        new_token = UserDBModel.encode_auth_token(user_id)
        response_object['token'] = new_token
        if user_id < 0:
            response_object['status'] = PROJECT_NOT_FOUND
            return response_object, 404
        response_object['project_id'] = project_id
        response_object['user_id'] = user_id
        return response_object, 200
