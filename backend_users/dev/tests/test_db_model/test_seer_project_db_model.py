from prod.db_models.user_db_model import UserDBModel
from prod.db_models.user_project_db_model import UserProjectDBModel
from prod.db_models.seer_project_db_model import SeerProjectDBModel
from dev.aux_test import recreate_db


def test_seerprojectdbmodel_get_projects_of_seer_id_devuelve_lista_vacia_cuando_el_usuario_no_existe(
        test_app,
        test_database):
    """
    Dada una base de datos vacia
    Cuando invoco get_projects_of_seer_id(<id usuario>)
    Obtengo:
        []
    """
    session = recreate_db(test_database)
    id_project_list = SeerProjectDBModel.get_projects_of_seer_id(11)
    assert len(id_project_list) == 0


def test_seerprojectdbmodel_get_projects_of_seer_id_devuelve_lista_vacia_cuando_no_se_ha_solicitado_la_veedoria_del_usuario_en_ningun_proyecto(
        test_app,
        test_database):
    """
    Dada una base de datos
    Y un usuario registrado.
    Sin proyectos
    Cuando invoco get_projects_of_seer_id(<id usuario>)
    Obtengo:
        []
    """
    session = recreate_db(test_database)
    user_id = UserDBModel.add_user(name="un nombre",
                                   lastname="un apellido",
                                   email="un email",
                                   password="una password")
    id_project_list = SeerProjectDBModel.get_projects_of_seer_id(user_id)
    assert len(id_project_list) == 0


def test_seerprojectdbmodel_get_projects_of_seer_id_devuelve_lista_de_ids_de_proyectos_asociados_al_veedor(
        test_app,
        test_database):
    """
    Dada una base de datos
    Y un usuario registrado.
    Tras invocar a add_project_to_seer_id(<id usuario>, 19)
    Cuando invoco get_projects_of_seer_id(<id usuario>)
    Obtengo:
        [(19, false)]
    """
    session = recreate_db(test_database)
    user_id = UserDBModel.add_user(name="un nombre",
                                   lastname="un apellido",
                                   email="un email",
                                   password="una password")
    project_id = 19
    id_projects_list = SeerProjectDBModel.add_project_to_seer_id(
        user_id, project_id)
    assert len(id_projects_list) == 1
    assert id_projects_list[0][0] == project_id
    assert (not id_projects_list[0][1])
    id_projects_list = SeerProjectDBModel.get_projects_of_seer_id(user_id)
    assert len(id_projects_list) == 1
    assert id_projects_list[0][0] == project_id
    assert (not id_projects_list[0][1])
