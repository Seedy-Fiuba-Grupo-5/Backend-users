from flask import Blueprint
from flask_restful import Api, Resource

index_api = Blueprint("index_api", __name__)
api = Api(index_api)


class IndexResource(Resource):
    @staticmethod
    def get():
        response_object = {
            "GET /users":   "status_code 200 =>" +
                            "[{id: <integer>, " +
                            "name: <string>, " +
                            "lastName: <string>, " +
                            "email: <string>, " +
                            "active: <boolean>}]"
        }
        return response_object, 200


api.add_resource(IndexResource, "/")
