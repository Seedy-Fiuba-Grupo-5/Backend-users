from flask_restx import Namespace, Resource, fields
from prod.db_models.user_db_model import UserDBModel

ns = Namespace(
    'users/<int:user_id>',
    description='One user related operations'
)


@ns.route('')
@ns.param('user_id', 'The user identifier')
class UserResource(Resource):
    USER_NOT_EXIST_ERROR = 'This user does not exists'

    code_200_swg = ns.model('One user output 200', {
        "id": fields.Integer(description='The user id'),
        "name": fields.String(description="The user name"),
        "lastName": fields.String(description="The user last name"),
        "email": fields.String(description="The user email"),
        "active": fields.Boolean(description="The user status")
    })

    code_404_swg = ns.model('One user output 404', {
        'status': fields.String(example=USER_NOT_EXIST_ERROR)
    })

    @ns.marshal_with(code_200_swg, 200)
    @ns.response(404, USER_NOT_EXIST_ERROR, code_404_swg)
    def get(self, user_id):
        '''Get user data'''
        user = UserDBModel.query.get(user_id)
        if not user:
            ns.abort(404, status=self.USER_NOT_EXIST_ERROR)
        response_object = user.serialize()
        return response_object, 200
