import json
from prod.db_models.user_db_model import UserDBModel


def test_db_get_only_one_user_when_the_user_is_in_the_db(test_app,
                                                         test_database):
    session = test_database.session
    session.remove()
    test_database.drop_all()
    test_database.create_all()
    session.add(UserDBModel(name="Franco Martin",
                            lastname="Di Maria",
                            email="fdimaria@fi.uba.ar",
                            password="hola"))
    session.commit()
    client = test_app.test_client()
    response = client.get("/users/1")
    assert response is not None
    assert response.status_code == 200
