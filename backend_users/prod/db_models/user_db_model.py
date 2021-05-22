from prod import db
from sqlalchemy import Column, Integer


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

    # Funcion para verificar si la combinacion usuario-password existe.
    # POST: Devuelve True si es asi. False en caso contrario.
    @staticmethod
    def comprobar_relacion_usuario_pass(email,
                                        password):
        db = UserDBModel.query.filter_by(email=email,
                                         password=password)
        return db.count() != 0

    @staticmethod
    def get_id(email, password):
        id_solicitado = UserDBModel.query.filter_by(email=email,
                                                    password=password)
        return id_solicitado.with_entities(UserDBModel.id)


# Clase representativa del schema que almacena a cada uno de los
# usuarios en el sistema junto con los id de los proyectos que posee
class UserProjectDBModel(db.Model):
    __tablename__ = "user_project"

    user_id = Column(Integer,
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
            "id_usuario": self.user_id,
            "project_id": self.project_id
        }

    # Funcion para devolver todos los proyectos asociados a un usuario
    @staticmethod
    def obtener_proyectos_asociados_a_un_usuario(id_usuario):
        return UserProjectDBModel.query.filter_by(id_usuario=id_usuario)
