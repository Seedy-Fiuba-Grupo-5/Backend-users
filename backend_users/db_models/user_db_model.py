from backend_users import db


class UserDBModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(128),
                     nullable=False)

    last_name = db.Column(db.String(128),
                          nullable=False)

    email = db.Column(db.String(128),
                      unique=True,
                      nullable=False)

    active = db.Column(db.Boolean(),
                       default=True,
                       nullable=False)

    def __init__(self,
                 name,
                 last_name,
                 email):
        self.name = name
        self.last_name = last_name
        self.email = email
