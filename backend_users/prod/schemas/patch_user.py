from flask_restx import Model, fields

patch_user = Model('One user patch', {
    "id": fields.Integer(description='The user id'),
    "name": fields.String(description="The user name"),
    "lastName": fields.String(description="The user last name"),
    "email": fields.String(description="The user email"),
    "active": fields.Boolean(description="The user status"),
    "seer": fields.Boolean(description="The state of seer"),
    "expo_token": fields.String(descriptcion="The device expo_token")
})
