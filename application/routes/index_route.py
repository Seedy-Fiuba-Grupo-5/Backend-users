from flask import jsonify
from application import app


@app.route("/") 
def hello_world():
    return jsonify(hello="world")
