from flask import render_template, Blueprint

# Nombre de la variable a utilizar para denominar a la ruta
index_v1_bp = Blueprint("index_v1_bp", __name__)


# Funcion que devuelve el template asociado al inicio de la pagina
@index_v1_bp.route("/")
def hello_world():
    return render_template('start_screen.html')
