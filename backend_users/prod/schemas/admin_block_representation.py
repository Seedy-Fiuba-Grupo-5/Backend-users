from flask_restx import Model, fields

admin_block_representation = Model('BlockOutput200', {
    'id': fields.Integer(description='The admin id'),
    'token': fields.String(description='The admin session token')
})
