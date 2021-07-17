from flask_restx import Model, fields

message_code20 = Model('Messages between users output 20x', {
    "id_1": fields.Integer(description='One user id'),
    "id_2": fields.String(description="The other user"),
    "text": fields.String(description="The message between users"),
    "owner": fields.String(description="The user_id of the user who send the "
                                       "id"),
    "date": fields.Boolean(description="The date of the message")
})
