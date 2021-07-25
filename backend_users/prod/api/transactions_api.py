from flask_restx import Namespace, fields
from flask import request
from prod.api.base_resource import BaseResource
from prod.db_models.user_db_model import UserDBModel
from prod.db_models.user_project_db_model import UserProjectDBModel
from prod.db_models.transactions_db_model import TransactionsDBModel
from prod.exceptions import BusinessError, InvalidTransitionAmount
from prod.schemas.user_representation import user_representation
from prod.exceptions import UserBlockedError, InvalidTransitionType
from prod.schemas.user_repeated import user_repeated
from prod.schemas.constants import MISSING_VALUES_ERROR, REPEATED_USER_ERROR
from prod.schemas.constants import INVALID_TOKEN

ns = Namespace(
    name='transactions',
    description='All user transactions related operations'
)


@ns.route('')
class UsersTransactionListResource(BaseResource):

    REGISTER_FIELDS = ("user_id", "project_id", "amount", "type", "token")

    code_status = {
        UserBlockedError: (406, 'user_blocked')
    }

    body_swg = ns.model(user_representation.name, user_representation)

    code_20x_swg = ns.model('All transactions input 20x', {
        'transaction_id': fields.Integer(description='The transaction id'),
        'user_id': fields.Integer(description=('The user id associated with '
                                               'the transaction')),
        'projects_id': fields.Integer(description=('The project id associated '
                                                   'with the transaction')),
        'amount': fields.Integer(description='The amount of the transaction'),
        'type': fields.String(description='The type of the transaction')
    })

    code_400_swg = ns.model(user_repeated.name, user_repeated)

    code_409_swg = ns.model('UserOutput409', {
        'status': fields.String(example=REPEATED_USER_ERROR)
    })

    @ns.response(200, 'Success', fields.List(fields.Nested(code_20x_swg)))
    def get(self):
        """Get all transactions"""
        response_object =\
            [user.serialize() for user in TransactionsDBModel.query.all()]
        return response_object, 200

    @ns.expect(body_swg)
    @ns.response(201, 'Success', code_20x_swg)
    @ns.response(400, MISSING_VALUES_ERROR, code_400_swg)
    @ns.response(409, 'User already exists', code_409_swg)
    def post(self):
        """Create a new transaction"""

        try:
            data = request.get_json()
            missing_args = self.missing_values(data, self.REGISTER_FIELDS)
            if missing_args:
                ns.abort(400, status=MISSING_VALUES_ERROR,
                         missing_args=missing_args)

            token_deco = UserDBModel.decode_auth_token(data['token'])
            if isinstance(token_deco, str) or data['user_id'] != token_deco:
                ns.abort(404, status=INVALID_TOKEN)
            owner_id = UserProjectDBModel.get_user_of_project_id(
                data['project_id'])
            if owner_id < 0:
                ns.abort(404, status='project not found')
            if owner_id == data['user_id'] and data['type'] == 'support':
                ns.abort(
                    401, status=('An Project Owner cannot support '
                                 'his/her own project'))
            if owner_id != data['user_id'] and data['type'] == 'pay':
                ns.abort(
                    401, status='Only Project Owner can make Pay transactions')
            user_model = TransactionsDBModel.add_transaction(
                data['user_id'],
                data['project_id'],
                data['amount'],
                data['type'])

            response_object = user_model.serialize()
            return response_object, 201
        except InvalidTransitionAmount:
            ns.abort(403, status='Transaction amount must be bigger than 0')
        except InvalidTransitionType:
            ns.abort(403, status=('Transaction type must '
                                  'be either support or pay'))
        except BusinessError as e:
            code, status = self.code_status[e.__class__]
            ns.abort(code, status=status)
