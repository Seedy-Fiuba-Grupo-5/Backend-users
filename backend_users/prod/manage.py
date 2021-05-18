from flask.cli import FlaskGroup
from prod import create_app, db
from prod.db_models.user_db_model import UserDBModel
import os

app = create_app()
with app.app_context():
    db.create_all()

if os.getenv("FLASK_ENV") == 'development':
    from flask_cors import CORS
    CORS(app)

cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    """Seeds db with some initial data."""
    db.session.add(UserDBModel(name="Brian",
                               lastName="Zambelli Tello",
                               email="bzambelli@fi.uba.ar",
                               password="hola"))
    db.session.add(UserDBModel(name="Franco Martin",
                               lastName="Di Maria",
                               email="fdimaria@fi.uba.ar",
                               password="hola"))
    db.session.add(UserDBModel(name="Hugo",
                               lastName="Larrea",
                               email="hlarrea@fi.uba.ar",
                               password="hola"))
    db.session.add(UserDBModel(name="Juan Diego",
                               lastName="Balestieri",
                               email="jbalestieri@fi.uba.ar",
                               password="hola"))
    db.session.add(UserDBModel(name="Kevin",
                               lastName="Mendoza",
                               email="kmendoza@fi.uba.ar",
                               password="hola"))

    db.session.commit()


if __name__ == "__main__":
    cli()
