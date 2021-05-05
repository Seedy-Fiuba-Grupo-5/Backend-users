from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

# TODO Englobar esto
app = Flask(__name__)   # Permite configurar la API
#app.config.from_object("config.config.Config")
db = SQLAlchemy(app)    # Permite manipular la base de datos

# === Definicion de tablas la base de datos ===

# Clase que modela la base de datos user. Consta de un id, email y
# si esta activa
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True)
    email = db.Column(db.String(128),
                      unique=True,
                      nullable=False)
    active = db.Column(db.Boolean(),
                       default=True,
                       nullable=False)

    # Creacion de la tabla
    def __init__(self,
                 email):
        self.email = email

# Elimina todas las tablas actuales
db.drop_all()

# Crea todas las tablas
db.create_all()

# Agrega los cambios a la base de datos
db.session.commit()

# === Definicion de la API ===

@app.route("/")
# Sanity check por defecto
def hello_world():
    return jsonify(hello="world")


# Metodo para imprimir la tabla users de la base de datos
# PRE: Es necesario que la base de datos db exista
@app.route("/users")
def imprimir_base_de_datos():
    db2 = User.query.all()
    return render_template('users.html',
                           db=db2)


# Metodo para actualizar con un valor hardcodeado la base de datos
# PRE: Dada las caracteristicas de la base de datos, solo se puede
# ejecutar una vez.
@app.route("/update")
def update_db():
    db.session.add(User(email="bzambelli2@fi.uba.ar"))
    db.session.commit()
    return "Ha sido actualizado"
