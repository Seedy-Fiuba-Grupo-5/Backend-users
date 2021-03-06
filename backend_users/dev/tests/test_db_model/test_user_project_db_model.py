from prod.db_models.user_db_model import UserDBModel
from prod.db_models.user_project_db_model import UserProjectDBModel
from dev.aux_test import recreate_db


def test_userprojectdbmodel_get_projects_of_user_id_devuelve_lista_vacia_cuando_el_usuario_no_existe(
        test_app,
        test_database):
    """
    Dada una base de datos vacia
    Cuando invoco get_projects_of_user_id(<id usuario>)
    Obtengo:
        []
    """
    session = recreate_db(test_database)
    id_project_list = UserProjectDBModel.get_projects_of_user_id(11)
    assert len(id_project_list) == 0


def test_userprojectdbmodel_get_projects_of_user_id_devuelve_lista_vacia_cuando_el_usuario_no_tiene_proyectos(
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
    user_id = UserDBModel.add_user(name="un nombre",
                                   lastname="un apellido",
                                   email="un email",
                                   password="una password",
                                   expo_token="IGNOREXPO")
    id_project_list = UserProjectDBModel.get_projects_of_user_id(user_id)
    assert len(id_project_list) == 0


def test_userprojectdbmodel_get_projects_of_user_id_devuelve_lista_de_ids_de_proyectos_asociados_al_usuario(
        test_app,
        test_database):
    """
    Dada una base de datos
    Y un usuario registrado.
    Tras invocar a add_project_to_user_id(<id usuario>, 19)
    Cuando invoco get_projects_of_user_id(<id usuario>)
    Obtengo:
        [19]
    """
    session = recreate_db(test_database)
    user_id = UserDBModel.add_user(name="un nombre",
                                   lastname="un apellido",
                                   email="un email",
                                   password="una password",
                                   expo_token="IGNOREXPO")
    project_id = 19
    id_projects_list = UserProjectDBModel.add_project_to_user_id(
        user_id, project_id)
    assert len(id_projects_list) == 1
    assert id_projects_list[0] == project_id
    id_projects_list = UserProjectDBModel.get_projects_of_user_id(user_id)
    assert len(id_projects_list) == 1
    assert id_projects_list[0] == project_id


def test_userprojectdbmodel_add_project_devuelve_lista_vacia_cuando_el_usuario_no_existe(
        test_app,
        test_database):
    """
    Dada una base de datos vacia
    Cuando invoco a add_project_to_user_id(11, 19)
    Obtengo:
        []
    """
    session = recreate_db(test_database)
    assert UserProjectDBModel.add_project_to_user_id(11, 19) == []


def test_userprojectdbmodel_add_project_devuelve_lista_con_proyectos_cuando_el_proyecto_ya_esta_asociado_a_este_usuario(
        test_app,
        test_database):
    """
    Dada una base de datos vacia
    Con un usuario registrado.
    Tras invocar a add_project_to_user_id(<id usuario>, 19)
    Cuando invocar a add_project_to_user_id(<id usuario>, 19)
    Obtengo:
        [19]
    """
    session = recreate_db(test_database)
    user_id = UserDBModel.add_user(name="un nombre",
                                   lastname="un apellido",
                                   email="un email",
                                   password="una password",
                                   expo_token="IGNOREXPO")
    project_id = 19
    id_projects_list = UserProjectDBModel.add_project_to_user_id(
        user_id, project_id)
    assert len(id_projects_list) == 1
    assert id_projects_list[0] == project_id
    id_projects_list = UserProjectDBModel.add_project_to_user_id(
        user_id, project_id)
    assert len(id_projects_list) == 1
    assert id_projects_list[0] == project_id
    id_projects_list = UserProjectDBModel.get_projects_of_user_id(user_id)
    assert len(id_projects_list) == 1
    assert id_projects_list[0] == project_id
