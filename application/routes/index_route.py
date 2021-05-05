from flask import render_template
from application import app


@app.route("/") 
def hello_world():
    return render_template('pantalla_inicio.html')
