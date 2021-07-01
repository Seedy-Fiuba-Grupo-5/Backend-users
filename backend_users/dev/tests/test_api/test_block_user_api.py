import json
from prod.db_models.admin_db_model import AdminDBModel
from prod.db_models.user_db_model import UserDBModel
from dev.aux_test import recreate_db


def test_patchs_and_blocks_asociated_id_to_admin_in_empty_db(
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
        active = True
    Cuando PATCH "admins/users/1"
    se modifica active de True a False
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "tomate"
    }
    client.post(
        "/users",
        data=json.dumps(body),
        content_type="application/json",
    )
    response = client.patch()
    body_2 = {
        "id_admin": 1,
        "token": AdminDBModel.encode_auth_token(1)
    }
    response = client.patch("/admins/users/1", data=json.dumps(body_2),
                            content_type="application/json")
    assert response.status_code == 200


def test_patchs_blocks_and_unblocks_asociated_id_to_admin_in_empty_db(
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
        active = True
    Cuando PATCH "admins/users/1"
    se modifica active de True a False
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "tomate"
    }
    client.post(
        "/users",
        data=json.dumps(body),
        content_type="application/json",
    )
    response = client.patch()
    body_2 = {
        "id_admin": 1,
        "token": AdminDBModel.encode_auth_token(1)
    }
    response = client.patch("/admins/users/1", data=json.dumps(body_2),
                            content_type="application/json")
    assert response.status_code == 200
    response = client.patch("/admins/users/1", data=json.dumps(body_2),
                            content_type="application/json")
    assert response.status_code == 200


def test_GET_only_users_unblocked(test_app,
                                  test_database):
    """En este test, se muestra como solo se
     devolvuelve a los usuarios no bloqueados"""
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
        content_type="application/json",
    )
    client.post(
        "/users",
        data=json.dumps(body_2),
        content_type="application/json",
    )
    response = client.get("/users")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert len(data) == 2
    body_3 = {
        "id_admin": 1,
        "token": AdminDBModel.encode_auth_token(1)
    }
    response = client.patch("/admins/users/1", data=json.dumps(body_3),
                            content_type="application/json")
    assert response.status_code == 200
    response = client.get("/users")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert len(data) == 1
