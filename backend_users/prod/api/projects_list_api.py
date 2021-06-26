from flask_restx import Namespace
from prod.api.base_resource import BaseResource
from prod.schemas.project_not_found import project_not_found,\
    PROJECT_NOT_FOUND

ns = Namespace(
    'projects/<int:project_id>',
    description="User's projects related operations"
)


@ns.route('')
@ns.param('project_id', 'The project identifier')
class UsersProjectsListResource(BaseResource):
    code_404_sw = ns.model(project_not_found.name, project_not_found)

    @ns.response(404, PROJECT_NOT_FOUND, code_404_sw)
    def get(self, project_id):
        """Get project's data"""
        response_object = {'status': PROJECT_NOT_FOUND}
        return response_object, 404
