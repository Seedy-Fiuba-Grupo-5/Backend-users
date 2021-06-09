from flask_restx import Namespace, Resource, fields
from flask import request
from prod.db_models.user_db_model import UserDBModel
from prod.exceptions import BusinessError, UserNotFoundError,\
    WrongPasswordError


ns = Namespace(
    'users/login',
    description='Users login operations'
)


@ns.route('')
class UsersLoginResource(Resource):
    REQUIRED_VALUES = ['email', 'password']
    MISSING_ARGS_ERROR = 'missing_args'
    USER_NOT_FOUND_ERROR = 'user_not_found'
    WRONG_PASS_ERROR = 'wrong_password'

    code_status = {
        UserNotFoundError: (404, USER_NOT_FOUND_ERROR),
        WrongPasswordError: (401, WRONG_PASS_ERROR)
    }

    body_swg = ns.model('LoginInput', {
        'email': fields.String(required=True, description='The user email'),
        'password': fields.String(
            required=True, description='The user password')
    })

    code_200_swg = ns.model('LoginOutput200', {
        'email': fields.String(description='The user email'),
        'id': fields.Integer(description='The user id')
    })

    code_400_swg = ns.model('LoginOutput400', {
        'status': fields.String(example=MISSING_ARGS_ERROR)
    })

    code_401_swg = ns.model('LoginOutput401', {
        'status': fields.String(example=WRONG_PASS_ERROR)
    })

    code_404_swg = ns.model('LoginOutput404', {
        'status': fields.String(example=USER_NOT_FOUND_ERROR)
    })

    @ns.expect(body_swg)
    @ns.response(200, 'Success', code_200_swg)
    @ns.response(400, 'Missing parameters', code_400_swg)
    @ns.response(401, 'Wrong password', code_401_swg)
    @ns.response(404, 'User not found', code_404_swg)
    def post(self):
        try:
            data = request.get_json()
            missing_args = self.missing_values(data, self.REQUIRED_VALUES)
            if missing_args != []:
                ns.abort(400, status=self.MISSING_ARGS_ERROR,
                         missing_args=missing_args)
            id = UserDBModel.get_id_token(data['email'], data['password'])
            response_object = {"email": data['email'], "id": id}
            return response_object, 200
        except BusinessError as e:
            code, status = self.code_status[e.__class__]
            ns.abort(code, status=status)

    @staticmethod
    def missing_values(json, field_list):
        missing_values = []
        for value in field_list:
            if value not in json:
                missing_values.append(value)
        return missing_values
