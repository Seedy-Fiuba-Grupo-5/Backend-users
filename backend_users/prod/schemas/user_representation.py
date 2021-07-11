from flask_restx import Model, fields

user_representation = Model('UserRepresentation', {
    "name": fields.String(required=True, description="The user name"),
    "lastName": fields.String(
        required=True, description="The user last name"),
    "email": fields.String(required=True, description="The user email"),
    "active": fields.Boolean(required=True, description="The user status"),
    "seer": fields.Boolean(required=False, description="associated seer "
                                                       "status")
})
