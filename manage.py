from flask.cli import FlaskGroup
from backend_users import create_app, db
from backend_users.db_models.user_db_model import UserDBModel
from flask_cors import CORS

app = create_app()
with app.app_context():
    db.create_all()
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
                               email="bzambelli@fi.uba.ar"))
    db.session.add(UserDBModel(name="Franco Martin",
                               lastName="Di Maria",
                               email="fdimaria@fi.uba.ar"))
    db.session.add(UserDBModel(name="Hugo",
                               lastName="Larrea",
                               email="hlarrea@fi.uba.ar"))
    db.session.add(UserDBModel(name="Juan Diego",
                               lastName="Balestieri",
                               email="jbalestieri@fi.uba.ar"))
    db.session.add(UserDBModel(name="Kevin",
                               lastName="Mendoza",
                               email="kmendoza@fi.uba.ar"))

    db.session.commit()


if __name__ == "__main__":
    cli()
