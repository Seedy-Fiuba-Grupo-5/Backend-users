import json
from prod.db_models.admin_db_model import AdminDBModel
from dev.aux_test import recreate_db


def test_gets_asociated_id_to_admin_in_empty_db(
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
    Cuando GET "admins/1"
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
        "/admins",
        data=json.dumps(body),
        content_type="application/json"
    )
    response = client.get("/admins/1")
    assert response is not None
    assert response.status_code == 200
    user = json.loads(response.data.decode())
    assert user['id'] == 1
    assert user['name'] == "Franco Martin"
    assert user['lastName'] == "Di Maria"
    assert user['email'] == "fdimaria@fi.uba.ar"
    assert user['active'] is True


def test_dada_una_db_con_dos_usuarios_de_ids_1_y_2_get_a_url_users_barra_id_1_y_barra_id_2_devuelve_a_cada_uno_de_ellos(
        test_app,
        test_database):
    """
    Dada una base de datos
    Con 2 usuarios registrados con ids 1 y 2
    Cuando GET "admins/1"
    Entonces obtengo el usuario de id = 1
    Cuando GET "admins/2"
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
        "/admins",
        data=json.dumps(body_1),
        content_type="application/json"
    )
    client.post(
        "/admins",
        data=json.dumps(body_2),
        content_type="application/json"
    )
    response = client.get("/admins/1")
    data = json.loads(response.data.decode())
    assert response is not None
    assert response.status_code == 200
    assert len(data) == 5
    assert data["id"] == 1
    assert data["name"] == "Franco Martin"
    assert data["lastName"] == "Di Maria"
    assert data["email"] == "fdimaria@fi.uba.ar"
    assert data["active"] == True
    response = client.get("/admins/2")
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
    Cuando GET "admins/1"
    Entonces obtengo status 404
    Y obtengo el cuerpo:
        {"status": 'user_not_found'}
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    response = client.get("/admins/1")
    assert response is not None
    assert response.status_code == 404
    data = json.loads(response.data.decode())
    assert data['status'] == 'user_not_found'


def test_patch_user_con_nuevo_email_actualiza_solo_el_email(
        test_app, test_database):
    """
    Dada una base de datos vacia.
    Y un usuario registrado:
        'id': <id>
        'name': 'a name'
        'lastName: 'a lastName'
        'email': 'test@test.com'
    Cuando patch 'admins/<id>'
    Con cuerpo vacio
        'name' : 'another name'
     Entonces obtengo el cuerpo:
        'id': <id>
        'name': 'a name'
        'lastName: 'a lastName'
        'email': 'another@test.com'
    """
    session = recreate_db(test_database)
    old_profile = {'name': 'a name', 'lastName': 'a last name',
                   'email': 'test@test.com', 'password': 'a password',
                   'token': AdminDBModel.encode_auth_token(1)}
    client = test_app.test_client()
    post_resp = client.post("/admins", json=old_profile)
    post_data = json.loads(post_resp.data.decode())
    user_id = post_data['id']
    update_profile = {'email': 'another@test.com',
                      'token': AdminDBModel.encode_auth_token(1)}
    patch_resp = client.patch(
        "/admins/{}".format(user_id),
        json=update_profile
    )
    assert patch_resp.status_code == 200
    patch_data = json.loads(patch_resp.data.decode())
    assert patch_data['email'] == update_profile['email']
    for field in old_profile.keys():
        if field in ['email', 'password', 'token']:
            continue
        assert patch_data[field] == old_profile[field]
    assert patch_data['id'] == user_id


def test_patch_nuevo_mail_pero_ya_existente_entonces_error(
        test_app, test_database):
    """
    Dada una base de datos vacia.
    Y un usuario registrado:
        'id': <id>
        'name': 'a name'
        'lastName: 'a lastName'
        'email': 'test@test.com
    Cuando patch 'admins/<id>'
    Con cuerpo vacio
        'name' : 'another name'
     Entonces obtengo el cuerpo:
        'id': <id>
        'name': 'another name'
        'lastName: 'a lastName'
        'email': 'test@test.com
    """
    session = recreate_db(test_database)
    repeated_mail = 'repeated@test.com'
    other_profile = {'name': 'a name', 'lastName': 'a last name',
                     'email': repeated_mail, 'password': 'a password',
                     'token': AdminDBModel.encode_auth_token(1)}
    old_profile = {'name': 'a name', 'lastName': 'a last name',
                   'email': 'test@test.com', 'password': 'a password',
                   'token': AdminDBModel.encode_auth_token(1)}
    client = test_app.test_client()
    other_resp = client.post("/admins", json=other_profile)
    other_data = json.loads(other_resp.data.decode())
    other_id = other_data['id']
    other_it = other_data['token']
    old_resp = client.post("/admins", json=old_profile)
    old_data = json.loads(old_resp.data.decode())
    user_id = old_data['id']

    update_profile = {'email': repeated_mail,
                      'token': AdminDBModel.encode_auth_token(2)}
    patch_resp = client.patch(
        "/admins/{}".format(user_id),
        json=update_profile
    )
    assert patch_resp.status_code == 409
    patch_data = json.loads(patch_resp.data.decode())
    assert patch_data['status'] == 'repeated_email'

    re_other_resp = client.get(
        "/admins/{}".format(other_id)
    )
    re_other_data = json.loads(re_other_resp.data.decode())
    assert re_other_data['email'] == other_profile['email']


def test_patch_user_con_nuevo_nombre_actualiza_solo_el_nombre(
        test_app, test_database):
    """
    Dada una base de datos vacia.
    Y un usuario registrado:
        'id': <id>
        'name': 'a name'
        'lastName: 'a lastName'
        'email': 'test@test.com'
    Cuando patch 'admins/<id>'
    Con cuerpo
        'name' : 'another name'
        'token': <token>
    Entonces obtengo el cuerpo:
        'id': <id>
        'name': 'another name'
        'lastName: 'a lastName'
        'email': 'another@test.com'
    """
    session = recreate_db(test_database)
    old_profile = {'name': 'a name', 'lastName': 'a last name',
                   'email': 'test@test.com', 'password': 'a password',
                   'token': AdminDBModel.encode_auth_token(1)}
    client = test_app.test_client()
    post_resp = client.post("/admins", json=old_profile)
    post_data = json.loads(post_resp.data.decode())
    user_id = post_data['id']
    update_profile = {'name': 'another name',
                              'token': AdminDBModel.encode_auth_token(1)}
    patch_resp = client.patch(
        "/admins/{}".format(user_id),
        json=update_profile
    )
    assert patch_resp.status_code == 200
    patch_data = json.loads(patch_resp.data.decode())
    assert patch_data['name'] == update_profile['name']
    for field in old_profile.keys():
        if field in ['name', 'password', 'token']:
            continue
        assert patch_data[field] == old_profile[field]
    assert patch_data['id'] == user_id


def test_patch_user_con_nuevo_id_no_actualiza_ningun_campo(
        test_app, test_database):
    """
    Dada una base de datos vacia.
    Y un usuario registrado:
        'id': <id>
        'name': 'a name'
        'lastName: 'a lastName'
        'email': 'test@test.com'
    Cuando patch 'admins/<id>'
    Con cuerpo
        'id' : 400
        'token': <token>
    Entonces obtengo el cuerpo:
        'id': <id>
        'name': 'a name'
        'lastName: 'a lastName'
        'email': 'another@test.com'
    """
    session = recreate_db(test_database)
    old_profile = {'name': 'a name', 'lastName': 'a last name',
                   'email': 'test@test.com', 'password': 'a password',
                   'token': AdminDBModel.encode_auth_token(1)}
    client = test_app.test_client()
    post_resp = client.post("/admins", json=old_profile)
    post_data = json.loads(post_resp.data.decode())
    user_id = post_data['id']
    update_profile = {'id': 400,
                      'token': AdminDBModel.encode_auth_token(1)}
    patch_resp = client.patch(
        "/admins/{}".format(user_id),
        json=update_profile
    )
    assert patch_resp.status_code == 200
    patch_data = json.loads(patch_resp.data.decode())
    for field in old_profile.keys():
        if field in ['password', 'token']:
            continue
        assert patch_data[field] == old_profile[field]
    assert patch_data['id'] == user_id


def test_patch_user_con_nuevo_nombre_y_apellido_actualiza_unicamente_nombre_y_apellido(
        test_app, test_database):
    """
    Dada una base de datos vacia.
    Y un usuario registrado:
        'id': <id>
        'name': 'a name'
        'lastName: 'a lastName'
        'email': 'test@test.com'
    Cuando patch 'admins/<id>'
    Con cuerpo
        'id' : 400
        'token': <token>
    Entonces obtengo el cuerpo:
        'id': <id>
        'name': 'a name'
        'lastName: 'a lastName'
        'email': 'another@test.com'
    """
    session = recreate_db(test_database)
    old_profile = {'name': 'a name', 'lastName': 'a last name',
                   'email': 'test@test.com', 'password': 'a password',
                   'token': AdminDBModel.encode_auth_token(1)}
    client = test_app.test_client()
    post_resp = client.post("/admins", json=old_profile)
    post_data = json.loads(post_resp.data.decode())
    user_id = post_data['id']
    update_profile = {'name': 'another name',
                      'lastName': 'another lastName',
                      'token': AdminDBModel.encode_auth_token(1)}
    patch_resp = client.patch(
        "/admins/{}".format(user_id),
        json=update_profile
    )
    assert patch_resp.status_code == 200
    patch_data = json.loads(patch_resp.data.decode())
    assert patch_data['name'] == update_profile['name']
    assert patch_data['lastName'] == update_profile['lastName']
    for field in old_profile.keys():
        if field in ['name', 'lastName', 'password', 'token']:
            continue
        assert patch_data[field] == old_profile[field]
    assert patch_data['id'] == user_id
