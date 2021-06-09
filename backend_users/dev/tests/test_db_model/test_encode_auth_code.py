from prod.db_models.user_db_model import UserDBModel
from dev.aux_test import recreate_db


def test_returns_auth_token_given_user(test_app,
                                       test_database):
    """Este test muestra como se deben utilizar los tokens.
    Se agrega a la sesion, al usuario:
    name="Franco",
    lastname="Di Maria",
    email="fdimaria@fi.uba.ar",
    password="hola
    Para luego testear que su id tokenizado puede ser decodeado correctamente.
    """

    user = UserDBModel(name="Franco",
                       lastname="Di Maria",
                       email="fdimaria@fi.uba.ar",
                       password="hola"
                       )
    session = recreate_db(test_database)
    session.add(user)
    session.commit()
    assert 1 == user.id
    auth_token = user.encode_auth_token(user.id)
    assert(isinstance(auth_token, str))
    auth_token_decoded = user.decode_auth_token(auth_token)
    assert auth_token_decoded == 1
    return 0
