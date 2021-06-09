import datetime
import flask
import jwt
from prod import db
from prod.db_models.black_list_db import BlacklistToken
from sqlalchemy import Column
from sqlalchemy import exc
from prod.exceptions import RepeatedEmailError, UserNotFoundError,\
    WrongPasswordError


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

    # Constructor de la clase.
    # PRE: Name tiene que ser un string de a lo sumo 128 caracteres, al igual
    # que password, lastname y email.
    def __init__(self,
                 name,
                 lastname,
                 email,
                 password):
        self.name = name
        self.lastName = lastname
        self.email = email
        self.password = password

    def update(self, name, lastName, email, password):
        try:
            self.__init__(name, lastName, email, password)
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
            "active": self.active
        }

    @staticmethod
    # Devuelve el id asociado a la relacion e-mail--password
    # POST: Devuelve -1 Si no existe la relacion e-mail, password
    def get_id(email, password):
        associated_id = UserDBModel.query.filter_by(email=email,
                                                    password=password)
        if associated_id.count() == 0:
            return -1
        return associated_id.with_entities(UserDBModel.id)[0][0]

    @staticmethod
    def get_id_token(email, password):
        user_model = UserDBModel.query.filter_by(email=email).first()
        if user_model is None:
            raise UserNotFoundError
        if password != user_model.password:
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
                 password):
        try:
            db.session.add(UserDBModel(name=name,
                                       lastname=lastname,
                                       email=email,
                                       password=password))
            db.session.commit()
            return UserDBModel.get_id(email,
                                      password)
        except exc.IntegrityError:
            return -1

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        payload = {
            'exp': datetime.datetime.utcnow() +
            datetime.timedelta(days=0,
                               seconds=5000),
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


# Clase representativa del schema que almacena a cada uno de los
# usuarios en el sistema junto con los id de los proyectos que posee
class UserProjectDBModel(db.Model):
    __tablename__ = "user_project"

    user_id = Column(db.Integer,
                     db.ForeignKey('users.id'),
                     primary_key=True)

    project_id = db.Column(db.Integer,
                           primary_key=True)

    # Constructor de la clase.
    # PRE: Ambos id deben corresponderse con los creados en sus respectivas
    # bases de datos
    def __init__(self,
                 user_id,
                 project_id):
        self.user_id = user_id
        self.project_id = project_id

    # Funcion que devuelve el par id_usuario, id_proyecto.
    def serialize(self):
        return {
            "user_id": self.user_id,
            "project_id": self.project_id
        }

    @classmethod
    def add_project_to_user_id(cls,
                               user_id,
                               project_id):
        try:
            db.session.add(UserProjectDBModel(user_id, project_id))
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            # TODO: Considerar levantar un excepcion.
        return UserProjectDBModel.get_projects_of_user_id(user_id)

    @staticmethod
    def get_projects_of_user_id(user_id):
        projects_query = UserProjectDBModel.query.filter_by(user_id=user_id)
        id_projects_list = \
            [user_project.project_id for user_project in projects_query.all()]
        return id_projects_list
