import json
from dev.aux_test import recreate_db


def test_db_vacia_post_users_name_franco_martin_last_name_di_maria_email_fdimaria_password_tomate_entonces_registra_nuevo_usuario_con_id_1(
        test_app,
        test_database):
    """
    Dado una base de datos vacia
    Y una peticion:
        name = "Franco Martin"
        lastName = "Di Maria"
        email = "fdimaria@fi.uba.ar"
        password = "tomate"
    Cuando POST "/users"
    Entonces obtengo status 201
    Y obtengo cuerpo con 4 campos:
        name = "Franco Martin"
        lastName = "Di Maria"
        email = "fdimaria@fi.uba.ar"
        id = 1
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "tomate"
    }
    response = client.post(
        "/users",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 201
    register_info = json.loads(response.data.decode())
    assert len(register_info) == 4
    assert register_info["name"] == "Franco Martin"
    assert register_info["lastName"] == "Di Maria"
    assert register_info["email"] == "fdimaria@fi.uba.ar"
    assert register_info["id"] == 1


def test_db_con_mail_fdimaria_registrado_post_users_name_franco_martin_last_name_di_maria_email_fdimaria_password_tomate_entonces_obtengo_un_error(
        test_app,
        test_database):
    """
    Dada una base de datos
    Y un usuario registrado:
        name = "Franco Martin"
        lastName = "Di Maria"
        email = "fdimaria@fi.uba.ar"
        password = "tomate"
    Y una peticion
        name = "Franco Martin"
        lastName "Di Maria"
        email = "fdimaria@fi.uba.ar"
        password = "tomate"
    Cuando POST "/users"
    Entonces obtengo status 401
    Y obtengo cuerpo:
        'User already registered'
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "tomate"
    }
    # Primer registro
    client.post(
        "/users",
        data=json.dumps(body),
        content_type="application/json",
    )
    # Repeticion del registro
    response = client.post(
        "/users",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 401
    error = json.loads(response.data.decode())
    assert error == 'User already registered'


def test_db_vacia_post_url_users_datos_name_franco_martin_entonces_obtengo_un_error(
        test_app,
        test_database):
    """
    Dada una base de datos vacia
    Y una peticion
        name = "Franco Martin"
    Cuando POST "/users"
    Entonces obtengo status 400
    Y obtengo cuerpo:
        'User already registered'
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body = {"name": "Franco Martin"}
    response = client.post(
        "/users",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 400
    error = json.loads(response.data.decode())
    assert error == 'Missing values'


def test_db_con_unico_usuario_name_Franco_Martin_last_name_Di_Maria_mail_fdimaria_password_hola_GET_users_debe_retornar_lo_anterior_con_id_1(
        test_app,
        test_database):
    """
    Dada una base de datos
    Y un usuario registrado:
        name = "Franco Martin"
        lastName = "Di Maria"
        email = "fdimaria@fi.uba.ar"
        password = "hola"
    Cuando GET "/users"
    Entonces obtengo status 200
    Y obtengo cuerpo con 1 elemento
    Y el elemento tiene 4 campos:
        name = "Franco Martin"
        lastName = "Di Maria"
        email = "fdimaria@fi.uba.ar"
        id = 1
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
        content_type="application/json",
    )
    response = client.get("/users")
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert len(data) == 1
    user = data[0]
    assert user["name"] == "Franco Martin"
    assert user["lastName"] == "Di Maria"
    assert user["email"] == "fdimaria@fi.uba.ar"
    assert user["id"] == 1


def test_db_con_usuario1_name_Franco_Martin_last_name_Di_Maria_email_fdimaria_password_hola_usuario2_name_Brian_last_name_Zambelli_Tello_email_bzambelli_password_hola_GET_users_debe_retornar_ambos_usuarios_con_ids_1_y_2(
        test_app,
        test_database):
    """
    Dada una base de datos
    Y un usuario registrado:
        name = "Franco Martin"
        lastName = "Di Maria"
        email = "fdimaria@fi.uba.ar"
        password = "hola"
    Y otro usuario registrado:
        name = "Brian"
        lastName = "Zambelli Tello"
        email = "bzambelli@fi.uba.ar"
        password = "hola"
    Cuando GET "/users"
    Entonces obtengo status 200
    Y obtengo cuerpo con 2 elementos
    Y un elemento tiene 4 campos:
        name = "Franco Martin"
        lastName = "Di Maria"
        email = "fdimaria@fi.uba.ar"
        id = 1
    Y otro elemento tiene 4 campos:
        name = "Brian"
        lastName = "Zambelli Tello"
        email = "bzambelli@fi.uba.ar"
        id = 2
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
    user_franco = data[0]
    user_brian = data[1]
    assert user_franco["name"] == "Franco Martin"
    assert user_franco["lastName"] == "Di Maria"
    assert user_franco["email"] == "fdimaria@fi.uba.ar"
    assert user_franco["id"] == 1
    assert user_brian["name"] == "Brian"
    assert user_brian["lastName"] == "Zambelli Tello"
    assert user_brian["email"] == "bzambelli@fi.uba.ar"
    assert user_brian["id"] == 2