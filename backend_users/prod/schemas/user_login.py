from flask_restx import Model, fields

user_login = Model('LoginInput', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(
        required=True, description='The user password')
})
