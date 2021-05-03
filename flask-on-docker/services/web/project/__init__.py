from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2

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


"""@app.route("/imprimir_caso_actual")
def imprimir_base_de_datos():
    conn = psycopg2.connect(database="users", user="postgres",
                            password="postgres", host="localhost")
    print("connected")
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM hello_flask_dev")
    data = mycursor.fetchall()
    return render_template('v_timestamp.html', data=data)
"""
