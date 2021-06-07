from flask_restx import Namespace, Resource, fields
from prod.db_models.user_db_model import UserDBModel

ns = Namespace(
    'users/<int:user_id>',
    description='One user related operations'
)


@ns.route('')
@ns.param('user_id', 'The user identifier')
@ns.response(404, 'The user does not exists')
class UserResource(Resource):
    resp_model = ns.model('One user output', {
        "id": fields.Integer(description='The user id'),
        "name": fields.String(description="The user name"),
        "lastName": fields.String(description="The user last name"),
        "email": fields.String(description="The user email"),
        "active": fields.Boolean(description="The user status")
    })

    @ns.marshal_with(resp_model, 200)
    def get(self, user_id):
        '''Get user data'''
        user = UserDBModel.query.get(user_id)
        if not user:
            ns.abort(404, status='This user does not exists')
        response_object = user.serialize()
        return response_object, 200
