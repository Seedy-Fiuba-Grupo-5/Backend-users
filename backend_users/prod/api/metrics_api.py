from flask_restx import Namespace
from prod.api.base_resource import BaseResource
from prod.db_models.user_db_model import UserDBModel
from prod.db_models.seer_project_db_model import SeerProjectDBModel
from prod.schemas.user_code20 import user_code20
from prod.schemas.admin_representation import admin_representation
from prod.db_models.user_project_db_model import UserProjectDBModel

ns = Namespace(
    'users/metrics',
    description='Metrics of all users'
)


@ns.route('')
class MetricsResource(BaseResource):
    body_swg = ns.model(admin_representation.name, admin_representation)

    code_200_swg = ns.model(user_code20.name, user_code20)

    @ns.response(200, 'Success', code_200_swg)
    def get(self):
        """Get metrics data"""
        response_object = {}
        list_of_user = [user.id for user in UserDBModel.query.all()]
        if len(list_of_user) == 0:
            response_object['percentage_blocked'] = 0
            response_object['percentage_with_project'] = 0
            response_object['percentage_seer'] = 0
            return response_object, 200
        list_of_blocked = \
            [user.id for user in UserDBModel.query.all() if
             user.active is False]
        list_of_seer = [user.id for user in SeerProjectDBModel.query.all() if
                        user.accepted is True]
        response_object['percentage_blocked'] = \
            len(list_of_blocked) / len(list_of_user)
        list_of_user_with_projects = \
            [user.user_id for user in UserProjectDBModel.query.all()]
        response_object['percentage_with_project'] = \
            len(list_of_user_with_projects) / len(list_of_user)
        response_object['percentage_seer'] = \
            len(list_of_seer) / len(list_of_user)
        return response_object, 200
