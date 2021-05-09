from backend_users import db


# Clase que modela la base de datos user. Consta de un id, email y
# si esta activa
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True)
    email = db.Column(db.String(128),
                      unique=True,
                      nullable=False)
    active = db.Column(db.Boolean(),
                       default=True,
                       nullable=False)

    # Creacion de la tabla
    def __init__(self,
                 email):
        self.email = email
