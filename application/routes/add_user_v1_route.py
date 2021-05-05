from application import app, db
from flask import render_template


# Metodo para actualizar con un valor hardcodeado la base de datos
# PRE: Dada las caracteristicas de la base de datos, solo se puede
# ejecutar una vez.
@app.route("/v1/add/new_user")
def add_user():
    return render_template('add_user.html')
