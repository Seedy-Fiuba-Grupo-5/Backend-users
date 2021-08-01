from prod import db
from sqlalchemy import Column
from sqlalchemy import exc


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

    @staticmethod
    def get_user_of_project_id(project_id):
        user_project = UserProjectDBModel\
            .query\
            .filter_by(project_id=project_id)\
            .first()
        if user_project is None:
            return -1
        return user_project.user_id
