from flask_restx import Namespace, Resource, fields
from flask import request
from prod.db_models.user_db_model import UserProjectDBModel

ns = Namespace(
    'users/<int:user_id>/projects', 
    description="User's projects related operations"
)

@ns.route('')
@ns.param('user_id', 'The user identifier')
class UsersProjectsListResource(Resource):

    body_swg = ns.model('User projects input', {
        'user_id': fields.Integer(required=True, description='The user id'),
        'project_id': fields.Integer(
            required=True, description='The project id'),
    })

    code_20x_swg = ns.model('User projects input 20x', {
        'user_id': fields.Integer(description='The user id'),
        'project_id': fields.List(
            fields.Integer(description='One of the user projects id')
        ) 
    })

    @ns.marshal_with(code_20x_swg, code=200)
    def get(self, user_id):
        id_projects_list =\
            UserProjectDBModel.get_projects_of_user_id(user_id)
        response_object = {
            "user_id": user_id,
            "project_id": id_projects_list
        }
        return response_object, 200

    @ns.expect(body_swg)
    @ns.marshal_with(code_20x_swg, code=201)
    def post(self, user_id):
        data = request.get_json()
        id_projects_list = UserProjectDBModel.add_project_to_user_id(
                                data['user_id'], data['project_id'])
        response_object = {
            "user_id": data['user_id'],
            "project_id": id_projects_list
        }
        # TODO: Considerar devolver errores
        return response_object, 201
