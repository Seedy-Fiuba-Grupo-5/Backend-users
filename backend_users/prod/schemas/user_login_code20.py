from flask_restx import Model, fields

user_login_code20 = Model('LoginOutput200', {
        'email': fields.String(description='The user email'),
        'id': fields.Integer(description='The user id'),
        'token': fields.String(description='The user session token')
    })
