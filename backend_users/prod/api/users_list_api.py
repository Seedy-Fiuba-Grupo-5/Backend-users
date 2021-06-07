from flask_restx import Namespace, Resource, fields
from flask import request
from prod.db_models.user_db_model import UserDBModel

ns = Namespace(
    name='users',
    description='All users related operations'
)


@ns.route('')
class UsersListResource(Resource):
    REGISTER_FIELDS = ("name", "lastName", "email", "password")
    REPEATED_USER_ERROR = 'User already registered'
    MISSING_VALUES_ERROR = 'Missing values'

    resp_model = ns.model('One user output', {
        "id": fields.Integer(description='The user id'),
        "name": fields.String(description="The user name"),
        "lastName": fields.String(description="The user last name"),
        "email": fields.String(description="The user email"),
        "active": fields.Boolean(description="The user status")
    })

    body_model = ns.model('One user input', {
        "name": fields.String(required=True, description="The user name"),
        "lastName": fields.String(
            required=True, description="The user last name"),
        "email": fields.String(required=True, description="The user email"),
        "active": fields.Boolean(required=True, description="The user status")
    })

    @ns.marshal_with(resp_model, code=200, as_list=True,)
    def get(self):
        '''Get all users data'''
        response_object =\
            [user.serialize() for user in UserDBModel.query.all()]
        return response_object, 200

    @ns.expect(body_model)
    @ns.marshal_with(resp_model, 201)
    @ns.response(400, MISSING_VALUES_ERROR)
    @ns.response(401, REPEATED_USER_ERROR)
    def post(self):
        '''Create a new user'''
        data = request.get_json()
        if not self.check_values(data, self.REGISTER_FIELDS):
            ns.abort(400, status=self.MISSING_VALUES_ERROR)
        user_id = UserDBModel.add_user(data['name'],
                                       data['lastName'],
                                       data['email'],
                                       data['password'])
        if user_id == -1:
            ns.abort(401, status=self.REPEATED_USER_ERROR)
        response_object = UserDBModel.query.get(user_id)
        return response_object, 201

    @staticmethod
    def check_values(json, fields_list):
        for value in fields_list:
            if value not in json:
                return False
        return True
