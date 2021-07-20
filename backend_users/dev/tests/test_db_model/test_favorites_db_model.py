from prod.db_models.user_db_model import UserDBModel
from prod.db_models.favorites_db_model import FavoritesProjectDBModel
from dev.aux_test import recreate_db


def test_favoritesdbmodel_get__favorites_projects_of_user_id_devuelve_lista_vacia_cuando_el_usuario_no_existe(
        test_app,
        test_database):
    """
    Dada una base de datos vacia
    Cuando invoco get_favorites_of_user_id(<id usuario>)
    Obtengo:
        []
    """
    session = recreate_db(test_database)
    id_project_list = FavoritesProjectDBModel.get_favorites_of_user_id(11)
    assert len(id_project_list) == 0


def test_favoritesdbmodel_get_projects_of_user_id_devuelve_lista_vacia_cuando_el_usuario_no_tiene_favoritos_agregados(
        test_app,
        test_database):
    """
    Dada una base de datos
    Y un usuario registrado.
    Sin proyectos
    Cuando invoco get_favorites_of_user_id(<id usuario>)
    Obtengo:
        []
    """
    session = recreate_db(test_database)
    user_id = UserDBModel.add_user(name="un nombre",
                                   lastname="un apellido",
                                   email="un email",
                                   password="una password")
    id_project_list = FavoritesProjectDBModel.get_favorites_of_user_id(user_id)
    assert len(id_project_list) == 0


def test_favoritesdbmodel_get_projects_of_user_id_devuelve_lista_de_ids_de_proyectos_favoritos_del_usuario(
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
    id_projects_list = FavoritesProjectDBModel.add_project_to_favorites_of_user_id(
        user_id, project_id)
    assert len(id_projects_list) == 1
    assert id_projects_list[0] == project_id
    id_projects_list = FavoritesProjectDBModel.get_favorites_of_user_id(
        user_id)
    assert len(id_projects_list) == 1
    assert id_projects_list[0] == project_id
