import json
from dev.aux_test import recreate_db


def test_dado_post_users_login_con_email_y_password_validos_obtiene_id_y_token_valido(
    test_app,
    test_database):
    """
    Dado una base de datos.
    Y un usuario registrado:
        id = <id>
        name = "a name"
        lastName = "a last name"
        email = "test@test.com"
        password = "a password"
    Y una peticion:
        "email": "test@test.com"
        "password": "a password"
    Cuando POST "/users/login"
    Entonces obtengo status 200:
    Y obtengo cuerpo con 3 campos:
        "email": "test@test.com"
        "id": <id>
        "token": <token>
    """

    session = recreate_db(test_database)
    client = test_app.test_client()
    body_prev = {
        "name": "a name",
        "lastName": "a last name",
        "email": "test@test.com",
        "password": "a password",
        "expo_token": "IGNOREXPO"
    }
    resp_prev = client.post(
        "/users",
        data=json.dumps(body_prev),
        content_type="application/json",
    )
    assert resp_prev.status_code == 201
    data_prev = json.loads(resp_prev.data.decode())
    body = {
        "email": "test@test.com",
        "password": "a password",
        'expo_token': "IGNOREXPO"
    }
    response = client.post(
        "/users/login",
        data=json.dumps(body),
        content_type="application/json"
    )
    login_info = json.loads(response.data.decode())
    assert response.status_code == 200
    assert login_info["email"] == "test@test.com"
    assert login_info["id"] == data_prev['id']
    body_token = {
        'user_id': 1,
        "token": login_info['token']
    }
    resp_token = client.post(
        "users/auth",
        data=json.dumps(body_token),
        content_type="application/json"
    )
    token_info = json.loads(resp_token.data.decode())
    assert token_info['status'] == 'Valid token'


def test_post_users_login_con_email_inexistente_entonces_error_404(
    test_app,
    test_database):
    """
    Dado una base de datos con un usuario registrado:
        name = "a name"
        lastName = "a last name"
        email = "test@test.com"
        password = "a password"
    Y una peticion:
        email = "another@test.com"
        password = "a password"
    Cuando POST "/users/login"
    Entonces obtengo status 404
    Y obtengo cuerpo:
        {"status": 'user_not_found'}
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body_prev = {
        "name": "a name",
        "lastName": "a last name",
        "email": "test@test.com",
        "password": "a password",
        "expo_token": "IGNOREXPO"
    }
    client.post(
        "/users",
        data=json.dumps(body_prev),
        content_type="application/json",
    )
    body = {
        "email": "another@test.com",
        "password": "a password",
        "expo_token": "IGNOREXPO"
    }
    response = client.post(
        "/users/login",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data['status'] == 'user_not_found'


def test_dado_email_fdimaria_registrado_y_password_tomate_cuando_POST_a_url_users_barra_login_el_email_y_la_palabra_de_pase_manzana_obtengo_un_error_401(
    test_app,
    test_database):
    """
    Dado una base de datos con un usuario registrado:
        name = "Franco Martin"
        lastName = "Di Maria"
        email = "fdimaria@fi.uba.ar"
        password = "tomate"
    Y una peticion:
        email = "fdimaria@fi.uba.ar"
        password = "manzana"
    Cuando POST "/users/login"
    Entonces obtengo status 401
    Y obtengo cuerpo:
        {"status": 'wrong_password'}
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body_prev = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "tomate",
        "expo_token": "IGNOREXPO"
    }
    client.post(
        "/users",
        data=json.dumps(body_prev),
        content_type="application/json",
    )
    body = {
        "email": "fdimaria@fi.uba.ar",
        "password": "manzana",
        "expo_token": "IGNOREXPO"
    }
    response = client.post(
        "/users/login",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 401
    data = json.loads(response.data.decode())
    assert data['status'] == 'wrong_password'


def test_dado_email_fdimaria_registrado_y_palabra_de_pase_tomate_cuando_POST_a_url_users_barra_login_email_fdimaria_obtengo_un_error(
    test_app,
    test_database):
    """
    Dado una base de datos con un usuario registrado:
        name = "Franco Martin"
        lastName = "Di Maria"
        email = "fdimaria@fi.uba.ar"
        password = "tomate"
    Y una peticion:
        email = "fdimaria@fi.uba.ar"
    Cuando POST "/users/login"
    Entonces obtengo status 400
    Y obtengo cuerpo:
        "status" = 'missing_args'
        "missing_args" = ['password']
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body_prev = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "tomate"
    }
    client.post(
        "/users",
        data=json.dumps(body_prev),
        content_type="application/json",
    )
    body = {"email": "fdimaria@fi.uba.ar"}
    response = client.post(
        "/users/login",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert data['status'] == 'missing_args'
    assert 'email' not in data['missing_args']
    assert 'password' in data['missing_args']
