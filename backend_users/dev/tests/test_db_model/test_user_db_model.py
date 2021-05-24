from prod.db_models.user_db_model import UserDBModel


def test_get_minus_one_when_register_user_twice(
        test_app,
        test_database
):
    session = test_database.session
    session.remove()
    test_database.drop_all()
    test_database.create_all()
    assert 1 == UserDBModel.add_user(name="Franco", lastname="Di Maria",
                                     email="fdimaria@fi.uba.ar",
                                     password="hola")
    assert -1 == UserDBModel.add_user(name="Franco", lastname="Di Maria",
                                      email="fdimaria@fi.uba.ar",
                                      password="hola")


def test_get_id_only_when_pass_and_user_is_correct(test_app,
                                                   test_database
                                                   ):
    session = test_database.session
    session.remove()
    test_database.drop_all()
    test_database.create_all()
    session.add(UserDBModel(name="Franco Martin",
                            lastname="Di Maria",
                            email="fdimaria@fi.uba.ar",
                            password="hola"))
    session.commit()
    assert UserDBModel.get_id(
        "bzambelli@fi.uba.ar",
        "hola") == -1
    assert UserDBModel.get_id(
        "fdimaria@fi.uba.ar",
        "hola") is 1
    assert UserDBModel.get_id(
        "fdimaria@fi.uba.ar",
        "hola2") is -1
