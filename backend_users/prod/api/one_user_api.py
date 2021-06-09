from flask import request
from flask_restx import Namespace, Resource, fields
from prod.db_models.user_db_model import UserDBModel
from prod.exceptions.business_error import BusinessError
from prod.printers.error_printer import ErrorPrinter
from prod.printers.error_printer import REPEATED_EMAIL_ERROR

ns = Namespace(
    'users/<int:user_id>',
    description='One user related operations'
)


@ns.route('')
@ns.param('user_id', 'The user identifier')
class UserResource(Resource):
    USER_NOT_EXIST_ERROR = 'This user does not exists'

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
        'status': fields.String(example=USER_NOT_EXIST_ERROR)
    })

    code_409_swg = ns.model('UserOutput409', {
        'status': fields.String(example=REPEATED_EMAIL_ERROR)
    })

    @ns.marshal_with(code_200_swg, code=200)
    @ns.response(404, USER_NOT_EXIST_ERROR, code_404_swg)
    def get(self, user_id):
        """Get user data"""
        user = UserDBModel.query.get(user_id)
        if not user:
            ns.abort(404, status=self.USER_NOT_EXIST_ERROR)
        response_object = user.serialize()
        return response_object, 200

    @ns.expect(body_swg)
    @ns.marshal_with(code_200_swg, code=200)
    @ns.response(404, USER_NOT_EXIST_ERROR, code_404_swg)
    @ns.response(409, REPEATED_EMAIL_ERROR, code_409_swg)
    def patch(self, user_id):
        '''Update user data'''
        try:
            user = UserDBModel.query.get(user_id)
            if not user:
                ns.abort(404, status=self.USER_NOT_EXIST_ERROR)
            json = request.get_json()
            user.update(
                name=json.get('name', user.name),
                lastName=json.get('lastName', user.lastName),
                email=json.get('email', user.email),
                password=json.get('password', user.password)
            )
            user = UserDBModel.query.get(user_id)
            response_object = user.serialize()
            return response_object, 200
        except BusinessError as e:
            code, status = ErrorPrinter.print(e)
            ns.abort(code, status=status)
