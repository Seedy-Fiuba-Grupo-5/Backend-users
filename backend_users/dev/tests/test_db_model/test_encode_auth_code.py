from prod.db_models.user_db_model import UserDBModel
from dev.aux_test import recreate_db

def test_returns_auth_token_given_user(test_app,
                                       test_database):
    user =UserDBModel(name="Franco",
                lastname="Di Maria",
                email="fdimaria@fi.uba.ar",
                password="hola"
                )
    session = recreate_db(test_database)
    session.add(user)
    session.commit()
    auth_token = user.encode_auth_token(user.id)
    assert(isinstance(auth_token, bytes))
    return 0
