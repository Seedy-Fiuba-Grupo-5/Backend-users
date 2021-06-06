# from flask import Blueprint
# from flask_restful import Api, Resource
from flask_restx import Namespace, Resource, fields
from prod.db_models.user_db_model import UserDBModel

api = Namespace('', description='User related operations')

user_fields = api.model('One User', {
    "id": fields.Integer(description='The user id'),
    "name": fields.String(description="The user name"),
    "lastName": fields.String(description="The user last name"),
    "email": fields.String(description="The user email"),
    "active": fields.Boolean(description="The user active status")
})


@api.route('/users/<int:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'The user does not exists')
class UserResource(Resource):

    @api.doc('get_user_data')
    @api.marshal_list_with(user_fields)
    def get(self, user_id):
        '''Get user data'''
        user = UserDBModel.query.get(user_id)
        if not user:
            return 'This user does not exists', 404
        response_object = user.serialize()
        return response_object, 200
