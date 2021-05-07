from flask import render_template
from application import app


# Funcion que devuelve el template asociado al inicio de la pagina
@app.route("/")
def hello_world():
    return render_template('start_screen.html')
