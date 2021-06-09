from flask_restx import Resource


class BaseResource(Resource):
    @staticmethod
    def missing_values(json, field_list):
        missing_values = []
        for value in field_list:
            if value not in json:
                missing_values.append(value)
        return missing_values
