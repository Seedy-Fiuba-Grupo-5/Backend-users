from prod.db_models.user_db_model import UserDBModel
from dev.aux_test import recreate_db


def test_changed_status_of_blocked_user(test_app,
                                        test_database):
    """Este tests muestra como se bloquea a un usuario.
    Se agrega a la sesion, al usuario:
    name="Franco",
    lastname="Di Maria",
    email="fdimaria@fi.uba.ar",
    password="hola
    Se testea que su estado, al momento de crear sea valido.
    Luego, se bloquea y se verifica que efectivamente su estado
    Cambio
    """

    user = UserDBModel(name="Franco",
                       lastname="Di Maria",
                       email="fdimaria@fi.uba.ar",
                       password="hola",
                       seer2=False,
                       expo_token="IGNOREXPO"
                       )
    session = recreate_db(test_database)
    session.add(user)
    session.commit()
    assert user.active is True
    UserDBModel.flip_active_status(user.id)
    assert user.active is False


def test_change_again_status_from_blocked_to_unlocked(test_app,
                                                      test_database):
    """Este tests muestra como se desbloquea a un usuario.
        Se agrega a la sesion, al usuario:
        name="Franco",
        lastname="Di Maria",
        email="fdimaria@fi.uba.ar",
        password="hola
        Se testea que su estado, al momento de crear sea valido.
        Luego, se bloquea y se verifica que efectivamente su estado
        Cambio
        """

    user = UserDBModel(name="Franco",
                       lastname="Di Maria",
                       email="fdimaria@fi.uba.ar",
                       password="hola",
                       seer2=False,
                       expo_token="IGNOREXPO"
                       )
    session = recreate_db(test_database)
    session.add(user)
    session.commit()
    assert user.active is True
    UserDBModel.flip_active_status(user.id)
    assert user.active is False
    UserDBModel.flip_active_status(user.id)
    assert user.active is True
