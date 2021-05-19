from prod import db


# Clase representativa del schema que almacena a cada uno de los
# usuarios en el sistema. Cada entrada consta de un id, name, lastname, email
# y un estado activo que por defecto es True.
# Un usuario puede tener mas de un proyecto. Un proyecto no puede estar
# asociado a mas de un usuario
class UserProyectDBModel(db.Model):
    __tablename__ = "user_proyect"

    id = db.Column(db.Integer,
                   primary_key=True)

    proyect_id = db.Column(db.Integer,
                           primary_key=True)

    # Constructor de la clase.
    # PRE: Ambos id deben corresponderse con los creados en sus respectivas
    # bases de datos
    def __init__(self,
                 id_usuario,
                 id_proyecto):
        self.id = id_usuario
        self.proyect_id = id_proyecto

    # Funcion que devuelve el par id_usuario, id_proyecto.
    def serialize(self):
        return {
            "id_usuario": self.id,
            "id_proyecto": self.proyect_id
        }

    # Funcion para devolver todos los proyectos asociados a un usuario
    @staticmethod
    def obtener_proyectos_asociados_a_un_usuario(id_usuario):
        return UserProyectDBModel.query.filter_by(id_usuario=id_usuario)
