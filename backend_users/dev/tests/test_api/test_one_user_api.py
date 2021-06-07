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


def test_dada_una_db_con_dos_usuarios_de_ids_1_y_2_get_a_url_users_barra_id_1_y_barra_id_2_devuelve_a_cada_uno_de_ellos(
        test_app,
        test_database):
    """
    Dada una base de datos
    Con 2 usuarios registrados con ids 1 y 2
    Cuando GET "users/1"
    Entonces obtengo el usuario de id = 1
    Cuando GET "users/2"
    Entonces obtengo el usuario de id = 2
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body_1 = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "hola"
    }
    body_2 = {
        "name": "Brian",
        "lastName": "Zambelli Tello",
        "email": "bzambelli@fi.uba.ar",
        "password": "hola"
    }
    client.post(
        "/users",
        data=json.dumps(body_1),
        content_type="application/json"
    )
    client.post(
        "/users",
        data=json.dumps(body_2),
        content_type="application/json"
    )
    response = client.get("/users/1")
    data = json.loads(response.data.decode())
    assert response is not None
    assert response.status_code == 200
    assert len(data) == 5
    assert data["id"] == 1
    assert data["name"] == "Franco Martin"
    assert data["lastName"] == "Di Maria"
    assert data["email"] == "fdimaria@fi.uba.ar"
    assert data["active"] == True
    response = client.get("/users/2")
    data = json.loads(response.data.decode())
    assert response is not None
    assert response.status_code == 200
    assert len(data) == 5
    assert data["id"] == 2
    assert data["name"] == "Brian"
    assert data["lastName"] == "Zambelli Tello"
    assert data["email"] == "bzambelli@fi.uba.ar"
    assert data["active"] == True


def test_dada_una_db_vacia_get_a_url_users_barra_id_1_devuelve_un_error(
        test_app,
        test_database):
    """
    Dada una base de datos vacia
    Cuando GET "users/1"
    Entonces obtengo status 404
    Y obtengo el cuerpo:
        {"status": 'This user does not exists'}
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    response = client.get("/users/1")
    assert response is not None
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data['status'] == 'This user does not exists'
