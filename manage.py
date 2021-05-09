from flask.cli import FlaskGroup
from backend_users import create_app, db
from backend_users.tables.users_table import User

app = create_app()
with app.app_context():
    db.create_all()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    """Seeds db with some initial data."""
    db.session.add(User(email="user1@gmail.com"))
    db.session.add(User(email="user2@gmail.com"))
    db.session.add(User(email="user3@gmail.com"))
    db.session.add(User(email="user4@gmail.com"))
    db.session.add(User(email="user5@gmail.com"))
    db.session.commit()


if __name__ == "__main__":
    cli()
