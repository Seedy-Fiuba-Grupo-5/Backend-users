from flask_restx import Namespace, fields
from prod.api.base_resource import BaseResource
from prod.db_models.transactions_db_model import TransactionsDBModel


ns = Namespace(
    'users/<int:user_id>/supports',
    description="User's favorite projects related operations"
)


@ns.route('')
@ns.param('user_id', 'The user identifier')
class UserSupportsListResource(BaseResource):

    code_20x_swg = ns.model('All transactions input 20x', {
        'transaction_id': fields.Integer(description='The transaction id'),
        'user_id': fields.Integer(description='The user id \
        associated with '
                                              'the transaction'),
        'projects_id': fields.Integer(description='The project id \
        associated with the transaction'),
        'amount': fields.Integer(description='The amount of the transaction'),
        'type': fields.String(description='The type of the transaction')
    })

    @ns.response(200, 'Success', fields.List(fields.Nested(code_20x_swg)))
    def get(self, user_id):
        """Get User's favorite projects"""
        response_object =\
            [transaction.serialize()
             for transaction in TransactionsDBModel.query.filter_by(
                user_id=user_id,
                type='support').all()]
        return response_object, 200
