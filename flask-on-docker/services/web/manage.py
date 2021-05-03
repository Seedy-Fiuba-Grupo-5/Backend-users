from flask.cli import FlaskGroup
from project import app, db, User

# TODO Englobar clase
cli = FlaskGroup(app)


# Metodo para crear la base de datos
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# Metodo para agregar una entrada hardcodeada a la base de datos
# PRE: La base de datos debe haber sido creada con anterioridad
@cli.command("seed_db")
def seed_db():
    db.session.add(User(email="bzambelli@fi.uba.ar"))
    db.session.commit()


# Ni idea. TODO Ver que es esto.
if __name__ == "__main__":
    cli()
