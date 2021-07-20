from flask_restx import Namespace, fields
from flask import request
from prod.api.base_resource import BaseResource
from prod.db_models.user_db_model import UserDBModel
from prod.db_models.favorites_db_model import FavoritesProjectDBModel
from prod.schemas.constants import USER_NOT_FOUND_ERROR, USER_BLOCKED,\
    MISSING_VALUES_ERROR, INVALID_TOKEN
from prod.schemas.project_not_found import PROJECT_NOT_FOUND

ns = Namespace(
    'users/<int:user_id>/favorites',
    description="User's favorite projects related operations"
)


@ns.route('')
@ns.param('user_id', 'The seer identifier')
class UserFavoriteProjectsListResource(BaseResource):

    body_swg = ns.model('User projects input', {
        'project_id': fields.Integer(
            required=True, description='The project id'),
    })
    code_20x_swg = ns.model('User projects input 20x', {
        'user_id': fields.Integer(description='The user id'),
        'projects_id': fields.List(
            fields.Integer(description='One of the user projects id')
        )
    })

    @ns.response(200, 'Success', code_20x_swg)
    def get(self, user_id):
        """Get User's favorite projects"""
        user = UserDBModel.query.get(user_id)
        if not user:
            ns.abort(404, status=USER_NOT_FOUND_ERROR)
        projects =\
            FavoritesProjectDBModel.get_favorites_of_user_id(user_id)
        response_object = {
            "user_id": user_id,
            "projects_id": projects,
        }
        return response_object, 200

    @ns.expect(body_swg)
    @ns.response(201, 'Success', code_20x_swg)
    def post(self, user_id):
        """Add project to user favorites"""
        try:
            data = request.get_json()
            token_decoded = FavoritesProjectDBModel.decode_auth_token(
                data['token'])
            if token_decoded != user_id:
                ns.abort(404, status=INVALID_TOKEN)
            if FavoritesProjectDBModel.get_active_status(user_id) is False:
                ns.abort(401,
                         status=USER_BLOCKED)
            projects_info = FavoritesProjectDBModel.add_project_to_favorites_of_user_id(
                user_id, data['project_id'])
            response_object = {
                "user_id": user_id,
                "projects_id": projects_info,
                "token": FavoritesProjectDBModel.encode_auth_token(user_id)
            }
            return response_object, 201
        except KeyError:
            ns.abort(404, status=MISSING_VALUES_ERROR)
        except AttributeError:
            ns.abort(404, status=USER_NOT_FOUND_ERROR)

    @ns.expect(body_swg)
    @ns.response(200, 'Success', code_20x_swg)
    def delete(self, user_id):
        """Remove project to user favorites"""
        try:
            data = request.get_json()
            token_decoded = FavoritesProjectDBModel.decode_auth_token(
                data['token'])
            if token_decoded != user_id:
                ns.abort(404, status=INVALID_TOKEN)
            if FavoritesProjectDBModel.get_active_status(user_id) is False:
                ns.abort(401,
                         status=USER_BLOCKED)
            deleted = FavoritesProjectDBModel.delete(
                user_id, data['project_id'])
            if deleted:
                projects_info = \
                    FavoritesProjectDBModel.get_favorites_of_user_id(user_id)
                response_object = {
                    "user_id": user_id,
                    "projects_id": projects_info,
                    "token": FavoritesProjectDBModel.encode_auth_token(user_id)
                }
                return response_object, 200
            else:
                ns.abort(404, status=PROJECT_NOT_FOUND)
        except KeyError:
            ns.abort(404, status=MISSING_VALUES_ERROR)
