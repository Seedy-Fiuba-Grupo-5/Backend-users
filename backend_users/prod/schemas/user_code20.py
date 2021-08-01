from flask_restx import Model, fields

user_code20 = Model('One user output 20x', {
    "id": fields.Integer(description='The user id'),
    "name": fields.String(description="The user name"),
    "lastName": fields.String(description="The user last name"),
    "email": fields.String(description="The user email"),
    "active": fields.Boolean(description="The user status"),
    "seer": fields.Boolean(description="The state of seer")
})
