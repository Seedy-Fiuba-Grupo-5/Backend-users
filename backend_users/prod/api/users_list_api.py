from flask_restx import Namespace, fields
from flask import request
from prod.api.base_resource import BaseResource
from prod.db_models.user_db_model import UserDBModel
from prod.exceptions import BusinessError, RepeatedEmailError

ns = Namespace(
    name='users',
    description='All users related operations'
)


@ns.route('')
class UsersListResource(BaseResource):
    REGISTER_FIELDS = ("name", "lastName", "email", "password")
    MISSING_VALUES_ERROR = 'missing_args'
    REPEATED_USER_ERROR = 'repeated_email'

    code_status = {
        RepeatedEmailError: (409, REPEATED_USER_ERROR)
    }

    body_swg = ns.model('One user input', {
        "name": fields.String(required=True, description="The user name"),
        "lastName": fields.String(
            required=True, description="The user last name"),
        "email": fields.String(required=True, description="The user email"),
        "active": fields.Boolean(required=True, description="The user status")
    })

    code_20x_swg = ns.model('One user output 20x', {
        "id": fields.Integer(description='The user id'),
        "name": fields.String(description="The user name"),
        "lastName": fields.String(description="The user last name"),
        "email": fields.String(description="The user email"),
        "active": fields.Boolean(description="The user status")
    })

    code_400_swg = ns.model('One user output 400', {
        'status': fields.String(example=MISSING_VALUES_ERROR),
        'missing_args': fields.List(fields.String())
    })

    code_409_swg = ns.model('UserOutput409', {
        'status': fields.String(example=REPEATED_USER_ERROR)
    })

    @ns.response(200, 'Success', fields.List(fields.Nested(code_20x_swg)))
    def get(self):
        """Get all users data"""
        response_object =\
            [user.serialize() for user in UserDBModel.query.all()]
        return response_object, 200

    @ns.expect(body_swg)
    @ns.response(201, 'Success', code_20x_swg)
    @ns.response(400, MISSING_VALUES_ERROR, code_400_swg)
    @ns.response(409, 'User already exists', code_409_swg)
    def post(self):
        """Create a new user"""
        try:
            data = request.get_json()
            missing_args = self.missing_values(data, self.REGISTER_FIELDS)
            if missing_args != []:
                ns.abort(400, status=self.MISSING_VALUES_ERROR,
                         missing_args=missing_args)
            id = UserDBModel.add_user(data['name'],
                                      data['lastName'],
                                      data['email'],
                                      data['password'])
            user_model = UserDBModel.query.get(id)
            response_object = user_model.serialize()
            response_object['token'] = UserDBModel.encode_auth_token(id)
            return response_object, 201
        except BusinessError as e:
            code, status = self.code_status[e.__class__]
            ns.abort(code, status=status)
