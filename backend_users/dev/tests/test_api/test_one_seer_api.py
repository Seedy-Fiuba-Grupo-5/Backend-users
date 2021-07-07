import json
from prod.db_models.user_db_model import UserDBModel
from dev.aux_test import recreate_db

def test_dada_una_db_vacia_get_a_seers_barra_id_1_devuelve_user_not_found(test_app,
        test_database):
    """
    Dada una base de datos vacia
    Cuando GET "seers/1"
    Entonces obtengo status 404
    Y obtengo el cuerpo:
        "status": "user_not_found",
        "message": <mensaje de error>
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    response = client.get("/seers/1")
    assert response is not None
    assert response.status_code == 404
    user = json.loads(response.data.decode())
    assert user['status'] == "user_not_found"


def test_dada_una_db_con_usuario_de_id_1_sin_proyectos_donde_es_veedor_get_a_seers_barra_id_1_devuelve_user_not_found(test_app,
        test_database):
    """
    Dada una base de datos con un usuario
    que no tiene proyectos donde es veedor
    Cuando GET "seers/1"
    Entonces obtengo status 404
    Y obtengo el cuerpo:
        "status": "user_not_found",
        "message": <mensaje de error>
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
    response = client.get("/seers/1")
    assert response is not None
    assert response.status_code == 404
    user = json.loads(response.data.decode())
    assert user['status'] == "user_not_found"

def test_dada_una_db_con_usuario_de_id_1_post_a_seers_barra_id_1_con_token_incorrecto_devuelve_user_not_found(test_app,
        test_database):
    """
    Dada una base de datos con un usuario
    Cuando POST "seers/1" con cuerpo:
        "project_id": 3,
        "token": ""
    Entonces obtengo status 404
    Y obtengo el cuerpo:
        "status": "user_not_found",
        "message": <mensaje de error>
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
    body = {
        "project_id": 3,
        "token": ""
    }
    response = client.post("/seers/1",
        data=json.dumps(body),
        content_type="application/json")
    assert response is not None
    assert response.status_code == 404
    user = json.loads(response.data.decode())
    assert user['status'] == "user_not_found"

def test_dada_una_db_con_usuario_de_id_1_post_a_seers_barra_id_1_con_el_cuerpo_correcto_entonces_obtengo(test_app,
        test_database):
    """
    Dada una base de datos con un usuario
    Cuando Post "seers/1" con el token adecuado y un project_id = 1
    Entonces obtengo status 201
    Y obtengo el cuerpo:
        "user_id": 1,
        "projects_info": [[1, false]]
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
    body = {
        "token": UserDBModel.encode_auth_token(1),
        "project_id": 1
    }
    post_response = client.post("/seers/1",
        data=json.dumps(body),
        content_type="application/json")
    assert post_response is not None
    assert post_response.status_code == 201
    user = json.loads(post_response.data.decode())
    assert user['user_id'] == 1
    assert user["projects_info"][0][0] == 1
    assert not user["projects_info"][0][1]

    old_response = json.loads(post_response.data.decode())
    get_response = client.get("/seers/1")
    assert get_response.status_code == 200
    new_response = json.loads(get_response.data.decode())
    for field in old_response.keys():
        if field in ['token']:
            continue
        assert old_response[field] == new_response[field]
