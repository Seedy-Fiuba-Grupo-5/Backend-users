from flask import Blueprint

ping_v1_api = Blueprint("ping_v1_api", __name__)


@ping_v1_api.route('/v1/ping')
def ping_v1():
    return {"status": "success", "message": "pong!"}
