from prod.db_models.user_db_model import UserDBModel, UserProjectDBModel
from dev.aux_test import recreate_db

def test_userprojectdbmodel_get_projects_devuelve_lista_vacia_cuando_el_usuario_no_tiene_proyectos(
    test_app, 
    test_database):
    """
    Dada una base de datos
    Y un usuario registrado.
    Sin proyectos
    Cuando invoco get_projects_of_user_id(<id usuario>)
    Obtengo:
        []
    """
    session = recreate_db(test_database)
    user_id = UserDBModel.add_user( name="un nombre",
                                    lastname="un apellido",
                                    email="un email",
                                    password="una password")
    id_project_list = UserProjectDBModel.get_projects_of_user_id(user_id)
    assert len(id_project_list) == 0
