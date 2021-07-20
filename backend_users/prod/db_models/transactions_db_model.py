from prod import db
from sqlalchemy import exc
from prod.exceptions import InvalidTransitionType, InvalidTransitionAmount


# Clase representativa del schema que almacena a cada uno de los
# usuarios en el sistema. Cada entrada consta de un id, name, lastname, email
# y un estado activo que por defecto es True

TRANSACTION_TYPES = ['support', 'pay']


class TransactionsDBModel(db.Model):
    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer,
                               primary_key=True)

    user_id = db.Column(db.Integer,
                        nullable=False)

    project_id = db.Column(db.Integer, nullable=False)

    amount = db.Column(db.Integer, nullable=False)

    type = db.Column(db.String(128),
                     nullable=False)

    # Constructor de la clase.
    # PRE: Type tiene que ser un string de a lo sumo 128 caracteres,
    # tanto el usuario como el proyecto fueron previamente creados.

    def __init__(self,
                 user_id,
                 project_id,
                 amount,
                 type2,
                 ):
        self.user_id = user_id
        self.project_id = project_id
        self.amount = amount
        self.type = type2

    def update(self, user_id, project_id, amount, type2):
        try:
            self.__init__(user_id, project_id, amount, type2)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()

    def serialize(self):
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "amount": self.amount,
            "type": self.type
        }

    @classmethod
    def add_transaction(cls,
                        user_id,
                        project_id,
                        amount,
                        type2):
        if type2 not in TRANSACTION_TYPES:
            raise InvalidTransitionType
        if amount <= 0:
            raise InvalidTransitionAmount
        project_model = TransactionsDBModel(user_id, project_id, amount, type2)
        db.session.add(project_model)
        db.session.commit()
        db.session.refresh(project_model)
        return project_model
