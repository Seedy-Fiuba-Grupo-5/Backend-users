from flask_restx import Model, fields

message_code20 = Model('Messages between users output 20x', {
    "id_1": fields.Integer(description='One user id'),
    "token": fields.String(description='Token associated')
})
