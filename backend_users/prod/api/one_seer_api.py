from flask_restx import Namespace, fields
from flask import request
from prod.api.base_resource import BaseResource
from prod.db_models.seer_project_db_model import SeerProjectDBModel
from prod.schemas.constants import USER_NOT_FOUND_ERROR, USER_BLOCKED
from prod.schemas.constants import MISSING_VALUES_ERROR, INVALID_SEER_ID
from prod.schemas.constants import INVALID_TOKEN, SEER_PROJECT_NOT_FOUND
from prod.schemas.project_not_found import PROJECT_NOT_FOUND
from prod.db_models.user_project_db_model import UserProjectDBModel

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

    post_swg_body = ns.model('Seer Post Body', {
        'token': fields.String(description='A valid Token'),
        'project_id': fields.Integer(
            required=True, description='The project id'),
    })

    patch_swg_body = ns.model('Seer Patch Body', {
        'token': fields.String(description='A valid Token'),
        'project_id': fields.Integer(
            required=True, description='The project id'),
        'accepted': fields.Boolean(
            required=True, description='The project id'),
    })

    code_200_swg = ns.model('Seer projects input 20x', {
        'user_id': fields.Integer(description='The Seer id'),
        'projects_info': fields.List(
            fields.Raw(description='One of the Seer projects '
                                   'id and its status')
        ),
        'token': fields.String(description='A valid Token')
    })

    patch_200_swg_response = ns.model('Seer Patch response 200', {
        'user_id': fields.Integer(description='The Seer id'),
        'project_id': fields.Integer(
            required=True, description='The project id'),
        'accepted': fields.Boolean(
            required=True, description='The project id'),
        'token': fields.String(description='A valid Token')
    })

    @ns.response(200, 'Success', code_200_swg)
    def get(self, user_id):
        """Get Seer's projects"""
        projects_info =\
            SeerProjectDBModel.get_projects_of_seer_id(user_id)
        if len(projects_info) == 0:
            ns.abort(404, status=USER_NOT_FOUND_ERROR)
        response_object = {
            "user_id": user_id,
            "projects_info": projects_info,
        }
        return response_object, 200

    @ns.expect(post_swg_body)
    @ns.response(201, 'Success', code_200_swg)
    def post(self, user_id):
        """Add project to user"""
        try:
            data = request.get_json()
            token_decoded = SeerProjectDBModel.decode_auth_token(data['token'])
            if isinstance(token_decoded, str):
                ns.abort(404, status=INVALID_TOKEN)
            owner_id = UserProjectDBModel.get_user_of_project_id(
                data['project_id'])
            if owner_id == user_id:
                ns.abort(404, status=INVALID_SEER_ID)
            if SeerProjectDBModel.get_active_status(user_id) is False:
                ns.abort(401,
                         status=USER_BLOCKED)
            projects_info = SeerProjectDBModel.add_project_to_seer_id(
                user_id, data['project_id'])
            if len(projects_info) == 0:
                ns.abort(404, status=USER_NOT_FOUND_ERROR)
            response_object = {
                "user_id": user_id,
                "projects_info": projects_info,
                "token": SeerProjectDBModel.encode_auth_token(user_id)
            }
            # TODO: Considerar devolver errores
            return response_object, 201
        except KeyError:
            ns.abort(404, status=MISSING_VALUES_ERROR)
        except AttributeError:
            ns.abort(404, status=USER_NOT_FOUND_ERROR)

    @ns.expect(patch_swg_body)
    @ns.response(200, 'Success', patch_200_swg_response)
    def patch(self, user_id):
        """Update user data"""
        try:
            json = request.get_json()
            seer = SeerProjectDBModel.query.get((user_id, json['project_id']))
            if not seer:
                ns.abort(404, status=SEER_PROJECT_NOT_FOUND)
            token_decoded = SeerProjectDBModel.decode_auth_token(json['token'])
            if token_decoded != user_id:
                ns.abort(404, status=INVALID_TOKEN)
            if SeerProjectDBModel.get_active_status(user_id) is False:
                ns.abort(401,
                         status=USER_BLOCKED)
            seer.update(
                accepted=json.get('accepted', seer.accepted)
            )
            seer = SeerProjectDBModel.query.get((user_id, json['project_id']))
            response_object = seer.serialize()
            response_object['token'] = SeerProjectDBModel.encode_auth_token(
                user_id)
            return response_object, 200
        except KeyError:
            ns.abort(404, status=MISSING_VALUES_ERROR)

    @ns.expect(post_swg_body)
    @ns.response(200, 'Success', code_200_swg)
    def delete(self, user_id):
        try:
            json = request.get_json()
            token_decoded = SeerProjectDBModel.decode_auth_token(json['token'])
            if token_decoded != user_id:
                ns.abort(404, status=INVALID_TOKEN)
            if SeerProjectDBModel.get_active_status(user_id) is False:
                ns.abort(401,
                         status=USER_BLOCKED)
            deleted = SeerProjectDBModel.delete(user_id, json['project_id'])
            if deleted:
                projects_info = \
                    SeerProjectDBModel.get_projects_of_seer_id(user_id)
                response_object = {
                    "user_id": user_id,
                    "projects_info": projects_info,
                    "token": SeerProjectDBModel.encode_auth_token(user_id)
                }
                return response_object, 200
            else:
                ns.abort(404, status=PROJECT_NOT_FOUND)
        except KeyError:
            ns.abort(404, status=MISSING_VALUES_ERROR)
