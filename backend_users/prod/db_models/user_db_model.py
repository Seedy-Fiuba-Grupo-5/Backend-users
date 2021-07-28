import datetime

import flask
import jwt
from prod import db
from prod.db_models.black_list_db import BlacklistToken
from prod.exceptions import RepeatedEmailError, UserNotFoundError, \
    WrongPasswordError
from sqlalchemy import exc
from prod.encryptor import Encryptor


# Clase representativa del schema que almacena a cada uno de los
# usuarios en el sistema. Cada entrada consta de un id, name, lastname, email
# y un estado activo que por defecto es True
class UserDBModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.String(128),
                     nullable=False)

    lastName = db.Column(db.String(128),
                         nullable=False)

    email = db.Column(db.String(128),
                      unique=True,
                      nullable=False)

    active = db.Column(db.Boolean(),
                       default=True,
                       nullable=False)

    password = db.Column(db.String(128),
                         nullable=False)

    seer = db.Column(db.Boolean(),
                     default=False,
                     nullable=True)
    expo_token = db.Column(db.String(900),
                           default="")

    # Constructor de la clase.
    # PRE: Name tiene que ser un string de a lo sumo 128 caracteres, al igual
    # que password, lastname y email.
    def __init__(self,
                 name,
                 lastname,
                 email,
                 password,
                 seer2,
                 active=True,
                 ):

        self.name = name
        self.lastName = lastname
        self.email = email
        self.password = password
        self.active = active
        self.seer = seer2

    @staticmethod
    def add_expo_token(token,
                       associated_id):
        user = UserDBModel.query.filter_by(id=associated_id).first()
        user.expo_token = token
        db.session.commit()

    @staticmethod
    def get_expo_token(associated_id):
        user = UserDBModel.query.filter_by(id=associated_id).first()
        return user.expo_token

    @staticmethod
    def flip_active_status(associated_id):
        user = UserDBModel.query.filter_by(id=associated_id).first()
        if not user.active:
            user.active = True
        else:
            user.active = False
        db.session.commit()

    @staticmethod
    def flip_seer_status(associated_id):
        user = UserDBModel.query.filter_by(id=associated_id).first()
        if not user.seer:
            user.seer = True
        else:
            user.seer = False
        db.session.commit()

    @staticmethod
    def get_active_status(associated_id):
        user = UserDBModel.query.filter_by(id=associated_id).first()
        return user.active

    @staticmethod
    def get_associated_email(associated_id):
        user = UserDBModel.query.filter_by(id=associated_id).first()
        return user.email

    def update(self, name, lastName, email, password, seer):
        try:
            self.__init__(name, lastName, email, password, seer)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            raise RepeatedEmailError

    # Funcion que devuelve los datos relevantes de un usuario, serializado
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastName": self.lastName,
            "email": self.email,
            "active": self.active,
            "seer": self.seer
        }

    @staticmethod
    def get_id(email, password):
        user_model = UserDBModel.query.filter_by(email=email).first()
        if user_model is None:
            raise UserNotFoundError
        encryptor = Encryptor()
        password_db = encryptor.decrypt(user_model.password)
        if password != password_db:
            raise WrongPasswordError
        return user_model.id

    @staticmethod
    def check_id(associated_id):
        return UserDBModel.query.filter_by(id=associated_id).count() == 1

    @classmethod
    def add_user(cls,
                 name,
                 lastname,
                 email,
                 password,
                 seer=False):
        encryptor = Encryptor()
        password_encry = encryptor.encrypt(password)
        try:
            db.session.add(UserDBModel(name=name,
                                       lastname=lastname,
                                       email=email,
                                       password=password_encry,
                                       seer2=seer))
            db.session.commit()
            return UserDBModel.get_id(email,
                                      password)
        except exc.IntegrityError:
            db.session.rollback()
            raise RepeatedEmailError

    EXPIRATION_TIME = 86400  # 1 dia = 86400 segundos

    @classmethod
    def encode_auth_token(cls, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        payload = {
            'exp': datetime.datetime.utcnow() +
            datetime.timedelta(days=0,
                               seconds=cls.EXPIRATION_TIME),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            flask.current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        ).decode("utf-8")

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, flask.current_app.config.get(
                'SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
