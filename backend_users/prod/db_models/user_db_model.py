from prod import db
from sqlalchemy import Column
from sqlalchemy import exc


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

    # Funcion para devolver todos los proyectos asociados a un usuario
    @staticmethod
    def get_projects_associated_to_user_id(user_id):
        return UserProjectDBModel.query.filter_by(user_id=user_id)

    @classmethod
    def add_project_to_user_id(cls,
                               user_id,
                               project_id):
        try:
            db.session.add(UserProjectDBModel(user_id, project_id))
            db.session.commit()
            return True
        except exc.IntegrityError:
            return False

    @staticmethod
    def get_projects_of_user_id(user_id):
        projects_query = UserProjectDBModel.query.filter_by(user_id=user_id)
        id_projects_list =\
            [user_project.project_id for user_project in projects_query.all()]
        return id_projects_list
