from flask_restx import Namespace, fields
from flask import request
from prod.api.base_resource import BaseResource
from prod.db_models.admin_db_model import AdminDBModel
from prod.exceptions import BusinessError, RepeatedEmailError
from prod.schemas.user_representation import user_representation
from prod.schemas.user_code20 import user_code20
from prod.schemas.user_email_repeated import user_email_repeated
from prod.schemas.constants import MISSING_VALUES_ERROR, REPEATED_USER_ERROR


ns = Namespace(
    name='admins',
    description='All users related operations'
)


@ns.route('')
class AdminsListResource(BaseResource):
    REGISTER_FIELDS = ("name", "lastName", "email", "password")

    code_status = {
        RepeatedEmailError: (409, REPEATED_USER_ERROR)
    }

    body_swg = ns.model(user_representation.name, user_representation)

    code_20x_swg = ns.model(user_code20.name, user_code20)

    code_400_swg = ns.model('One user output 400', {
        'status': fields.String(example=MISSING_VALUES_ERROR),
        'missing_args': fields.List(fields.String())
    })

    code_409_swg = ns.model(user_email_repeated.name, user_email_repeated)

    @ns.response(200, 'Success', fields.List(fields.Nested(code_20x_swg)))
    def get(self):
        """Get all users data"""
        response_object =\
            [user.serialize() for user in AdminDBModel.query.all()]
        return response_object, 200

    @ns.expect(body_swg)
    @ns.response(201, 'Success', code_20x_swg)
    @ns.response(400, MISSING_VALUES_ERROR, code_400_swg)
    @ns.response(409, 'User already exists', code_409_swg)
    def post(self):
        """Create a new admin"""
        try:
            data = request.get_json()
            id = AdminDBModel.add_user(data['name'],
                                       data['lastName'],
                                       data['email'],
                                       data['password'])
            user_model = AdminDBModel.query.get(id)
            response_object = user_model.serialize()
            response_object['token'] = AdminDBModel.encode_auth_token(id)
            return response_object, 201
        except BusinessError as e:
            code, status = self.code_status[e.__class__]
            ns.abort(code, status=status)
