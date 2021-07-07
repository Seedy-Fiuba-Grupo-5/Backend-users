from prod import db
from sqlalchemy import Column
from sqlalchemy import exc
from prod.db_models.user_db_model import UserDBModel

# Clase representativa del schema que almacena a cada uno de los
# veedorres en el sistema junto con los id de los proyectos en los que cumple
# dicho rol o en los cuales dicha solicitud esta pendiente a ser aceptada


class SeerProjectDBModel(db.Model):
    __tablename__ = "seer_project"

    user_id = Column(db.Integer,
                     db.ForeignKey('users.id'),
                     primary_key=True)
    project_id = db.Column(db.Integer,
                           primary_key=True)
    # accepted es true solo si el veedor ha aceptado serlo para el
    # proyecto determinado
    # es false si dicha solicitud esta pendiente
    # si el veedor rechaza cumplor ese rol para el proyecto, la entrada debe
    # ser eliminada
    accepted = db.Column(db.Boolean(),
                         default=False,
                         nullable=False)

    # Constructor de la clase.
    # PRE: Ambos id deben corresponderse con los creados en sus respectivas
    # bases de datos
    def __init__(self,
                 user_id,
                 project_id, accepted=False):
        self.user_id = user_id
        self.project_id = project_id
        self.accepted = accepted

    def serialize(self):
        return {
            "user_id": self.user_id,
            "project_id": self.project_id,
            "accepted": self.accepted
        }

    @classmethod
    def add_project_to_seer_id(cls,
                               user_id,
                               project_id):
        try:
            db.session.add(SeerProjectDBModel(user_id, project_id))
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            # TODO: Considerar levantar un excepcion.
        return SeerProjectDBModel.get_projects_of_seer_id(user_id)

    def update(self, accepted):
        try:
            self.__init__(self.user_id, self.project_id, accepted)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()

    @staticmethod
    def get_projects_of_seer_id(user_id):
        projects_query = SeerProjectDBModel.query.filter_by(user_id=user_id)
        id_projects_list = \
            [(user_project.project_id, user_project.accepted) for
             user_project in projects_query.all()]
        return id_projects_list

    @staticmethod
    def get_seer_of_project_id(project_id):
        user_project = SeerProjectDBModel \
            .query \
            .filter_by(project_id=project_id) \
            .first()
        if user_project is None:
            return -1
        return user_project.user_id

    @staticmethod
    def delete(user_id, project_id):
        seer = SeerProjectDBModel.query.filter_by(
            user_id=user_id, project_id=project_id).first()
        deleted = False
        if seer:
            db.session.delete(seer)
            db.session.commit()
            deleted = True
        return deleted

    @classmethod
    def encode_auth_token(cls, user_id):
        return UserDBModel.encode_auth_token(user_id)

    @staticmethod
    def decode_auth_token(auth_token):
        return UserDBModel.decode_auth_token(auth_token)

    @staticmethod
    def get_active_status(associated_id):
        return UserDBModel.get_active_status(associated_id)
