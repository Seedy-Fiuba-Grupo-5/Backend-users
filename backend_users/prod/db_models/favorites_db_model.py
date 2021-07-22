from prod import db
from sqlalchemy import Column
from sqlalchemy import exc
from prod.db_models.user_db_model import UserDBModel

# Clase representativa del schema que almacena a cada uno de los
# ids de los proyectos que un determinado usuario ha marcado como favorito


class FavoritesProjectDBModel(db.Model):
    __tablename__ = "user_favorite_projects"

    user_id = Column(db.Integer,
                     db.ForeignKey('users.id'),
                     primary_key=True)
    project_id = db.Column(db.Integer,
                           primary_key=True)

    # Constructor de la clase.
    # PRE: Ambos id deben corresponderse con los creados en sus respectivas
    # bases de datos
    def __init__(self,
                 user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "project_id": self.project_id
        }

    @classmethod
    def add_project_to_favorites_of_user_id(cls,
                                            user_id,
                                            project_id):
        try:
            db.session.add(FavoritesProjectDBModel(user_id, project_id))
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            # TODO: Considerar levantar un excepcion.
        return FavoritesProjectDBModel.get_favorites_of_user_id(user_id)

    def update(self, accepted):
        try:
            self.__init__(self.user_id, self.project_id, accepted)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()

    @staticmethod
    def get_favorites_of_user_id(user_id):
        projects_query = FavoritesProjectDBModel.query.filter_by(
            user_id=user_id)
        id_projects_list = \
            [user_project.project_id for user_project in projects_query.all()]
        return id_projects_list

    @staticmethod
    def delete(user_id, project_id):
        seer = FavoritesProjectDBModel.query.filter_by(
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
