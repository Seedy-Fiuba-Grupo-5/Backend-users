from prod.db_models.user_db_model import UserDBModel
from dev.aux_test import recreate_db


def test_se_devuelve_un_menos_uno_cuando_se_quiere_registrar_un_mail_ya_usado(
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
