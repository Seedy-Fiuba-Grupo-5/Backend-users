from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

# TODO Englobar esto
app = Flask(__name__)
# app.config.from_object("application.config.Config")
db = SQLAlchemy(app)

# Importar endpoints
from application.routes import *


# Elimina todas las tablas actuales
db.drop_all()

# Crea todas las tablas
db.create_all()

# Agrega los cambios a la base de datos
db.session.commit()
