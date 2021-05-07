from flask import render_template
from application import app
from application.tables.users_table import User


# Metodo para imprimir la tabla users de la base de datos
# PRE: Es necesario que la base de datos db exista
@app.route("/v1/users")
def imprimir_base_de_datos():
    db2 = User.query.all()
    return render_template('users.html',
                           db=db2)
