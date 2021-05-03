from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
#from models import *

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/")
# Sanity check por defecto
def hello_world():
    return jsonify(hello="world")


@app.route("/prueba")
def hello_world_brian():
    return jsonify(hello="Brian")


@app.route("/imprimir_caso_actual")
def imprimir_base_de_datos():
    db2 = User.query.all()
    return render_template('users.html', db=db2)
