from flask_restx import Namespace, fields
from flask import request
from prod.api.base_resource import BaseResource
from prod.db_models.seer_project_db_model import SeerProjectDBModel
from prod.schemas.constants import USER_NOT_FOUND_ERROR
from prod.schemas.project_not_found import PROJECT_NOT_FOUND

ns = Namespace(
    'seers/<int:user_id>',
    description="Seer's projects related operations"
)


@ns.route('')
@ns.param('user_id', 'The seer identifier')
class SeersProjectsListResource(BaseResource):

    body_swg = ns.model('User projects input', {
        'project_id': fields.Integer(
            required=True, description='The project id'),
    })

    code_20x_swg = ns.model('Seer projects input 20x', {
        'user_id': fields.Integer(description='The Seer id'),
        'projects_info': fields.List(
            fields.Raw(description='One of the Seer projects '
                                   'id and its status')
        )
    })

    @ns.response(200, 'Success', code_20x_swg)
    def get(self, user_id):
        """Get Seer's projects"""
        projects_info =\
            SeerProjectDBModel.get_projects_of_seer_id(user_id)
        if len(projects_info) == 0:
            ns.abort(404, status=USER_NOT_FOUND_ERROR)
        response_object = {
            "user_id": user_id,
            "project_info": projects_info,
        }
        return response_object, 200

    @ns.expect(body_swg)
    @ns.response(201, 'Success', code_20x_swg)
    def post(self, user_id):
        """Add project to user"""
        data = request.get_json()
        projects_info = SeerProjectDBModel.add_project_to_seer_id(
            user_id, data['project_id'])
        if len(projects_info) == 0:
            ns.abort(404, status=USER_NOT_FOUND_ERROR)
        response_object = {
            "user_id": user_id,
            "projects_info": projects_info
        }
        # TODO: Considerar devolver errores
        return response_object, 201

    @ns.expect(body_swg)
    @ns.response(200, 'Success', code_20x_swg)
    def patch(self, user_id):
        """Update user data"""
        try:
            json = request.get_json()
            seer = SeerProjectDBModel.query.get((user_id, json['project_id']))
            if not seer:
                ns.abort(404, status=USER_NOT_FOUND_ERROR)
            seer.update(
                accepted=json.get('accepted', seer.accepted)
            )
            seer = SeerProjectDBModel.query.get((user_id, json['project_id']))
            response_object = seer.serialize()
            return response_object, 200
        except KeyError:
            ns.abort(404, status=self.MISSING_VALUES_ERROR)

    @ns.expect(body_swg)
    @ns.response(200, 'Success', code_20x_swg)
    def delete(self, user_id):
        json = request.get_json()
        deleted = SeerProjectDBModel.delete(user_id, json['project_id'])
        if deleted:
            projects_info = \
                SeerProjectDBModel.get_projects_of_seer_id(user_id)
            response_object = {
                "user_id": user_id,
                "project_info": projects_info,
            }
            return response_object, 200
        else:
            ns.abort(404, status=PROJECT_NOT_FOUND)
