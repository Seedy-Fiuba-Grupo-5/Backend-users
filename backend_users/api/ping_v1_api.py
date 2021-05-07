from flask import Blueprint
#from flask_restful import Api, Resource

ping_v1_bp = Blueprint("ping_v1_bp", __name__)

@ping_v1_bp.route('/v1/ping')
def ping_v1():
    return {"status": "success", "message": "pong!"}

