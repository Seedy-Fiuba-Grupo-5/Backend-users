from flask import render_template
from backend_users.tables.users_table import User
from flask import Blueprint

users_v1_api = Blueprint("users_v1_api", __name__)


# Metodo para imprimir la tabla users de la base de datos
# PRE: Es necesario que la base de datos db exista
@users_v1_api.route('/v1/users')
def imprimir_base_de_datos():
    db2 = User.query.all()
    return render_template('users.html',
                           db=db2)
