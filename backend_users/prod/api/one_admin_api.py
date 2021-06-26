from flask import request
from flask_restx import Namespace, fields
from prod.api.base_resource import BaseResource
from prod.db_models.admin_db_model import AdminDBModel
from prod.exceptions import BusinessError, RepeatedEmailError
from prod.schemas.constants import USER_NOT_FOUND_ERROR, REPEATED_EMAIL_ERROR
ns = Namespace(
    'admins/<int:user_id>',
    description='One user related operations'
)


@ns.route('')
@ns.param('user_id', 'The user identifier')
class AdminResource(BaseResource):
    REQUIRED_VALUES = ['name', 'lastName', 'email', 'password', 'token']

    code_status = {
        RepeatedEmailError: (409, 'repeated_email')
    }

    body_swg = ns.model('NotRequiredUserInput', {
        "name": fields.String(description="The user new name"),
        "lastName": fields.String(description="The user new last name"),
        "email": fields.String(description="The user new email"),
        "password": fields.String(description="The user new password")
    })

    code_200_swg = ns.model('UserOutput200', {
        "id": fields.Integer(description='The user id'),
        "name": fields.String(description="The user name"),
        "lastName": fields.String(description="The user last name"),
        "email": fields.String(description="The user email"),
        "active": fields.Boolean(description="The user status")
    })

    code_404_swg = ns.model('UserOutput404', {
        'status': fields.String(example=USER_NOT_FOUND_ERROR)
    })

    code_409_swg = ns.model('UserOutput409', {
        'status': fields.String(example=REPEATED_EMAIL_ERROR)
    })

    @ns.response(200, 'Success', code_200_swg)
    @ns.response(404, USER_NOT_FOUND_ERROR, code_404_swg)
    def get(self, user_id):
        """Get user data"""
        user = AdminDBModel.query.get(user_id)
        if not user:
            ns.abort(404, status=USER_NOT_FOUND_ERROR)
        response_object = user.serialize()
        return response_object, 200

    @ns.expect(body_swg)
    @ns.response(200, 'Success', code_200_swg)
    @ns.response(404, USER_NOT_FOUND_ERROR, code_404_swg)
    @ns.response(409, REPEATED_EMAIL_ERROR, code_409_swg)
    def patch(self, user_id):
        """Update user data"""
        try:
            user = AdminDBModel.query.get(user_id)
            if not user:
                ns.abort(404, status=USER_NOT_FOUND_ERROR)
            json = request.get_json()
            token_decoded = AdminDBModel.decode_auth_token(json['token'])
            if token_decoded != user_id:
                ns.abort(404, status=USER_NOT_FOUND_ERROR)
            user.update(
                name=json.get('name', user.name),
                lastName=json.get('lastName', user.lastName),
                email=json.get('email', user.email),
                password=json.get('password', user.password)
            )
            user = AdminDBModel.query.get(user_id)
            response_object = user.serialize()
            response_object['token'] = AdminDBModel.encode_auth_token(user_id)
            return response_object, 200
        except BusinessError as e:
            code, status = self.code_status[e.__class__]
            ns.abort(code, status=status)
        except KeyError:
            ns.abort(404, status=self.MISSING_VALUES_ERROR)
