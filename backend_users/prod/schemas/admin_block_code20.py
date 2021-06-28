from flask_restx import Model, fields

admin_block_code20 = Model('BlockOutput200', {
        'id': fields.Integer(description='The user id'),
        'token': fields.String(description='The user session token')
    })
