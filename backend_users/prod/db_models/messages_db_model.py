import datetime
from prod import db
from prod.db_models.user_db_model import UserDBModel


# Clase representativa del schema que almacena a cada uno de los
# usuarios en el sistema. Cada entrada consta de un id, name, lastname, email
# y un estado activo que por defecto es True
class MessagesDBModel(db.Model):
    __tablename__ = "messages"
    column_not_exist_in_db = db.Column(db.Integer,
                                       primary_key=True)
    id_1 = db.Column(db.Integer)

    id_2 = db.Column(db.Integer)

    text = db.Column(db.String(280),
                     nullable=False)

    date = db.Column(db.DateTime,
                     nullable=False)
    owner = db.Column(db.Integer,
                      nullable=False)

    # Constructor de la clase.
    # PRE: Name tiene que ser un string de a lo sumo 128 caracteres, al igual
    # que password, lastname y email.
    def __init__(self,
                 id_1,
                 id_2,
                 text,
                 owner):
        self.id_1 = id_1
        self.id_2 = id_2
        self.text = text
        self.owner = owner
        self.date = datetime.datetime.now()

    def serialize(self):
        email = ""
        if self.text != "TESTMESSAGE":
            email = UserDBModel.get_associated_email(self.owner)
        return {
            "email": email,
            "id_1": self.id_1,
            "id_2": self.id_2,
            "text": self.text,
            "owner": self.owner,
            "date": self.date.strftime("%m/%d/%Y, %H:%M:%S")
        }

    @staticmethod
    def get_messages_from_user(requested_id):
        query = MessagesDBModel.query.filter_by(id_2=requested_id)
        if len(query.all()) == 0:
            return {}
        response_object = \
            [message.serialize() for message in query.all()]
        return response_object, 200

    @classmethod
    def add_message(cls,
                    id_1,
                    id_2,
                    message):
        db.session.add(MessagesDBModel(id_1=id_1,
                                       id_2=id_2,
                                       text=message,
                                       owner=id_1))
        db.session.commit()
