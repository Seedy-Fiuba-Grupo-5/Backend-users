import json
from prod.db_models.user_db_model import UserDBModel
from dev.aux_test import recreate_db


def test_dada_una_db_con_usuario_de_id_1_get_a_url_users_barra_id_1_devuelve_a_este_usuario(
    test_app,
    test_database):
    """
    Dada una base de datos
    Y un usuario registrado:
        name = "Franco Martin"
        lastName = "Di Maria"
        email = "fdimaria@fi.uba.ar"
        password = "hola"
        id = 1
    Cuando GET "users/1"
    Entonces obtengo status 200
    Y obtengo el cuerpo:
        id = 1,
        name = "Franco Martin"
        lastName = "Di Maria"
        email = "fdimaria@fi.uba.ar"
        active = True
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "hola"
    }
    client.post(
        "/users",
        data=json.dumps(body),
        content_type="application/json"
    )
    response = client.get("/users/1")
    assert response is not None
    assert response.status_code == 200
    user = json.loads(response.data.decode())
    assert user['id'] == 1
    assert user['name'] == "Franco Martin"
    assert user['lastName'] == "Di Maria"
    assert user['email'] == "fdimaria@fi.uba.ar"
    assert user['active'] == True


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
