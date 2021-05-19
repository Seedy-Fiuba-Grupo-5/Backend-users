from prod.db_models.user_db_model import UserDBModel


def test_devuelve_true_cuando_la_relacion_usuario_pass_es_correcta(test_app,
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
    assert UserDBModel.comprobar_relacion_usuario_pass(
        "bzambelli@fi.uba.ar",
        "hola") is False
    assert UserDBModel.comprobar_relacion_usuario_pass(
        "fdimaria@fi.uba.ar",
        "hola") is True
