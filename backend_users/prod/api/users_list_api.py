from flask_restx import Namespace, Resource, fields
from flask import request
from prod.db_models.user_db_model import UserDBModel
from prod.exceptions import BusinessError, RepeatedEmailError

ns = Namespace(
    name='users',
    description='All users related operations'
)


@ns.route('')
class UsersListResource(Resource):
    REGISTER_FIELDS = ("name", "lastName", "email", "password")
    MISSING_VALUES_ERROR = 'Missing values'
    REPEATED_USER_ERROR = 'repeated_user'

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
        'status': fields.String(example=MISSING_VALUES_ERROR)
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
            if not self.check_values(data, self.REGISTER_FIELDS):
                ns.abort(400, status=self.MISSING_VALUES_ERROR)
            id = UserDBModel.add_user(data['name'],
                                      data['lastName'],
                                      data['email'],
                                      data['password'])
            user_model = UserDBModel.query.get(id)
            response_object = user_model.serialize()
            return response_object, 201
        except BusinessError as e:
            code, status = self.code_status[e.__class__]
            ns.abort(code, status=status)

    @staticmethod
    def check_values(json, fields_list):
        for value in fields_list:
            if value not in json:
                return False
        return True
