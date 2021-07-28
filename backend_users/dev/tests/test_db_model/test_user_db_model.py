from prod.db_models.user_db_model import UserDBModel
from prod.exceptions import RepeatedEmailError, UserNotFoundError, \
    WrongPasswordError
from dev.aux_test import recreate_db


def test_userdbmodel_add_user_dos_veces_al_mismo_usuario_devuelve_menos_1(
    test_app,
    test_database):
    """
    Dada una base de datos vacia
    Invocar UserDBModel.add_user(<usuario 1>) => 1
    Invocar otra vez UserDBModel.add_user(<usuario 1>) => -1
    """
    session = recreate_db(test_database)
    assert 1 == UserDBModel.add_user(name="Franco", lastname="Di Maria",
                                     email="fdimaria@fi.uba.ar",
                                     password="hola",
                                     expo_token="IGNOREXPO")
    try:
        UserDBModel.add_user(name="Franco", lastname="Di Maria",
                             email="fdimaria@fi.uba.ar",
                             password="hola",
                             expo_token="IGNOREXPO")
        assert False
    except RepeatedEmailError:
        assert True


def test_get_id_only_when_pass_and_user_is_correct(
    test_app,
    test_database):
    """
    Dada una base de datos
    Y un usuario registrado:
        name = "Franco Martin"
        lastName = "Di Maria"
        email = "fdimaria@fi.uba.ar"
        password = "hola"
        Id = 1
    Invocar UserDBModel.get_id("bzambelli@fi.uba.ar", "hola") => -1
    Invocar UserDBModel.get_id("fdimaria@fi.uba.ar", "hola")  =>  1
    Invocar UserDBModel.get_id("fdimaria@fi.uba.ar", "hola2") => -1
    """
    session = recreate_db(test_database)
    UserDBModel.add_user(name="Franco Martin",
                         lastname="Di Maria",
                         email="fdimaria@fi.uba.ar",
                         password="hola",
                         expo_token="IGNOREXPO")

    session.commit()
    try:
        UserDBModel.get_id(
            "bzambelli@fi.uba.ar",
            "hola")
        assert False
    except UserNotFoundError:
        assert True
    assert UserDBModel.get_id(
        "fdimaria@fi.uba.ar",
        "hola") is 1
    try:
        UserDBModel.get_id(
            "fdimaria@fi.uba.ar",
            "hola2")
        assert False
    except WrongPasswordError:
        assert True


def test_obtain_valid_id_from_database(test_app, test_database):
    """Dada una base de datos con un usuario registrado
    se busca obtener un retorno valido al preguntar por un
    id que deberia estar
    name = "Franco Martin"
    lastName = "Di Maria"
    email = "fdimaria@fi.uba.ar"
    password = "hola"
    Id = 1
    Invocar UserDBModel.check_id(1) => True"""
    session = recreate_db(test_database)
    session.add(UserDBModel(name="Franco Martin",
                            lastname="Di Maria",
                            email="fdimaria@fi.uba.ar",
                            password="hola",
                            seer2=False,
                            expo_token="IGNOREXPO"))
    session.commit()
    assert UserDBModel.check_id(1) is True
