from flask_restx import Namespace, fields
from flask import request
from prod.api.base_resource import BaseResource
from prod.db_models.messages_db_model import MessagesDBModel
from prod.db_models.user_db_model import UserDBModel
from prod.exceptions import BusinessError, RepeatedEmailError, UserBlockedError
from prod.schemas.message_representation import message_representation
from prod.schemas.constants import MISSING_VALUES_ERROR, REPEATED_USER_ERROR
from prod.schemas.constants import USER_NOT_FOUND_ERROR, MISSING_ARGS_ERROR
from prod.schemas.message_code20 import message_code20
from prod.expo.messenger import Messenger

ns = Namespace(
    name='messages/<int:user_id>',
    description='All users related operations'
)


@ns.route('')
class UsersListResource(BaseResource):
    REGISTER_FIELDS = ("id_1", "message", "token")
    GET_FIELDS = ('id', 'token')

    code_status = {
        RepeatedEmailError: (409, REPEATED_USER_ERROR),
        UserBlockedError: (406, 'user_blocked')
    }

    body_swg = ns.model(message_representation.name, message_representation)

    code_20x_swg = ns.model(message_code20.name, message_code20)

    code_400_swg = ns.model('MessageOutput400', {
        'status': fields.String(example=MISSING_ARGS_ERROR),
        'missing_args': fields.List(fields.String())
    })

    @ns.response(400, MISSING_VALUES_ERROR, code_400_swg)
    @ns.response(200, 'Success', fields.List(fields.Nested(code_20x_swg)))
    def get(self, user_id):
        """Get all messages data"""
        try:
            json = request.get_json()
            token_decoded = UserDBModel.decode_auth_token(json['token'])
            if token_decoded != user_id:
                ns.abort(404, status=USER_NOT_FOUND_ERROR)
            response_object = MessagesDBModel.get_messages_from_user(
                user_id)
            return response_object, 200
        except KeyError:
            ns.abort(400, status=MISSING_VALUES_ERROR)

    @ns.expect(body_swg)
    @ns.response(201, 'Success', code_20x_swg)
    @ns.response(400, MISSING_VALUES_ERROR, code_400_swg)
    def post(self, user_id):
        """Adds a new message a new user"""
        try:
            data = request.get_json()
            missing_args = self.missing_values(data, self.REGISTER_FIELDS)
            if missing_args:
                ns.abort(400, status=MISSING_VALUES_ERROR,
                         missing_args=missing_args)
            token_decoded = UserDBModel.decode_auth_token(data['token'])
            id_user = data['id_1']
            if token_decoded != id_user:
                ns.abort(404, status=USER_NOT_FOUND_ERROR)
            MessagesDBModel.add_message(id_user,
                                        user_id,
                                        data['message'])
            token = UserDBModel.get_expo_token(data['id_1'])
            messenger = Messenger()
            messenger.send_push_message(token,
                                        data['message'],
                                        'nothing')
            response_object = {'user_1': data['id_1'],
                               'token': UserDBModel.encode_auth_token(
                                   data['id_1'])}
            return response_object, 201
        except BusinessError as e:
            code, status = self.code_status[e.__class__]
            ns.abort(code, status=status)
