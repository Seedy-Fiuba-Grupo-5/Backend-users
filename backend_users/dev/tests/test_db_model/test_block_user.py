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
                       password="hola"
                       )
    session = recreate_db(test_database)
    session.add(user)
    session.commit()
    assert user.active is True
    UserDBModel.block(user.id)
    assert user.active is False
