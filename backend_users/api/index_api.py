from flask import Blueprint

index_api = Blueprint("index_api", __name__)


@index_api.route('/')
def ping_v1():
    return {"status": "success", "message": "pong!"}
