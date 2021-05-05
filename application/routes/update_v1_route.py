from application import app, db
from application.tables.users_table import User

# Metodo para actualizar con un valor hardcodeado la base de datos
# PRE: Dada las caracteristicas de la base de datos, solo se puede
# ejecutar una vez.
@app.route("/v1/update")
def update_db():
    db.session.add(User(email="bzambelli2@fi.uba.ar"))
    db.session.commit()
    return "Ha sido actualizado"
