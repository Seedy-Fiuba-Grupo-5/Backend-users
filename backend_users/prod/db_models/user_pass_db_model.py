from prod import db


class UserPassDBModel(db.Model):
    __tablename__ = "user_pass"

    email = db.Column(db.String(128),
                      primary_key=True,
                      unique=True,
                      nullable=False)

    password = db.Column(db.String(12),
                         nullable=False)

    def __init__(self,
                 email,
                 password):
        self.password = password
        self.email = email

    @staticmethod
    def comprobar_relacion_usuario_pass(email,
                                        password):
        return UserPassDBModel.query.filter_by(email=email,
                                               password=password) is not None
