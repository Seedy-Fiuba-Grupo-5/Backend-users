import responses
from application import app, db
from application.tables.users_table import User

# Creacion de base de datos vacia. (Si se utiliza la funcion .all() no devuelve None
def test_creacion(self):
	users = User.query.get(1)
	assert users is None

def test_agregar_dato(self):
	db.session.add(User(email="bzambelli@fi.uba.ar"))
	users = User.query.get(1)