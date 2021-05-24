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


def test_se_obtiene_solo_el_primer_usuario(test_app,
                                           test_database):
    session = test_database.session
    session.remove()
    test_database.drop_all()
    test_database.create_all()
    session.add(UserDBModel(name="Franco Martin",
                            lastname="Di Maria",
                            email="fdimaria@fi.uba.ar",
                            password="hola"))
    session.add(UserDBModel(name="Martin",
                            lastname="Maria",
                            email="fdimaria2@fi.uba.ar",
                            password="hola"))
    session.commit()
    client = test_app.test_client()
    response = client.get("/users/1")
    data = json.loads(response.data.decode())
    assert response is not None
    assert response.status_code == 200
    assert len(data) == 5
    assert data["id"] == 1
    assert data["name"] == "Franco Martin"
    response = client.get("/users/2")
    data = json.loads(response.data.decode())
    assert response is not None
    assert response.status_code == 200
    assert len(data) == 5
    assert data["id"] == 2
    assert data["name"] == "Martin"
