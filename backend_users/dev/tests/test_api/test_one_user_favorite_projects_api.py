import json
from prod.db_models.user_db_model import UserDBModel
from dev.aux_test import recreate_db


def test_dada_una_db_vacia_get_a_users_barra_id_1_barra_favorites_devuelve_user_not_found(test_app,
                                                                                          test_database):
    """
    Dada una base de datos vacia
    Cuando GET "/users/1/favorites"
    Entonces obtengo status 404
    Y obtengo el cuerpo:
        "status": "user_not_found",
        "message": <mensaje de error>
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    response = client.get("/users/1/favorites")
    assert response is not None
    assert response.status_code == 404
    user = json.loads(response.data.decode())
    assert user['status'] == "user_not_found"


def test_dada_una_db_con_usuario_de_id_1_sin_proyectos_favoritos_get_a_users_barra_id_1_barra_favorites_devuelve_una_lista_vacia(test_app,
                                                                                                                                 test_database):
    """
    Dada una base de datos con un usuario
    que no tiene proyectos donde es veedor
    Cuando GET "/users/1/favorites"
    Entonces obtengo status 404
    Y obtengo el cuerpo:
        "user_id": 1,
        "projects_id": []
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
    response = client.get("/users/1/favorites")
    assert response is not None
    assert response.status_code == 200
    user = json.loads(response.data.decode())
    assert user['user_id'] == 1
    assert len(user['projects_id']) == 0


def test_dada_una_db_con_usuario_de_id_1_post_a_users_barra_id_1_barra_favorites_con_el_cuerpo_correcto_entonces_obtengo(test_app,
                                                                                                                         test_database):
    """
    Dada una base de datos con un usuario
    Cuando Post "/users/1/favorites" con el token adecuado y un project_id = 1
    Entonces obtengo status 201
    Y obtengo el cuerpo:
        "user_id": 1,
        "projects_id": [
            1
        ],
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
    post_response = client.post("/users/1/favorites",
                                data=json.dumps(body),
                                content_type="application/json")
    assert post_response is not None
    assert post_response.status_code == 201
    user = json.loads(post_response.data.decode())
    assert user['user_id'] == 1
    assert user["projects_id"][0] == 1

    old_response = json.loads(post_response.data.decode())
    get_response = client.get("/users/1/favorites")
    assert get_response.status_code == 200
    new_response = json.loads(get_response.data.decode())
    for field in old_response.keys():
        if field in ['token']:
            continue
        assert old_response[field] == new_response[field]


def test_dada_una_db_con_usuario_de_id_1_con_un_proyecto_favorito_de_id_1_al_hacer_un_delete_de_dicho_id_el_usuario_ya_no_es_veedor_en_ningun_proyecto(test_app,
                                                                                                                                                       test_database):
    """
    Dada una base de datos con un usuario
    Cuando Delete "/users/1/favorites" con el token adecuado y un project_id = 1
    Entonces obtengo status 201
    Y obtengo el cuerpo:
        "user_id": 1,
        "projects_info": []
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body_usuario = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "hola"
    }
    client.post(
        "/users",
        data=json.dumps(body_usuario),
        content_type="application/json"
    )

    body_post = {
        "token": UserDBModel.encode_auth_token(1),
        "project_id": 1
    }
    client.post("/users/1/favorites",
                data=json.dumps(body_post),
                content_type="application/json")

    body_delete = {
        "token": UserDBModel.encode_auth_token(1),
        "project_id": 1,
    }
    delete_response = client.delete("/users/1/favorites",
                                    data=json.dumps(body_delete),
                                    content_type="application/json")

    assert delete_response is not None
    assert delete_response.status_code == 200
    user = json.loads(delete_response.data.decode())
    assert user['user_id'] == 1
    assert user["projects_id"] == []


def test_dada_una_db_con_usuario_de_id_1_con_un_proyecto_favorito_de_id_1_al_hacer_un_delete_de_un_proyecto_con_id_2_se_obtiene_project_not_found(test_app,
                                                                                                                                                  test_database):
    """
    Dada una base de datos con un usuario
    Cuando Delete "/users/1/favorites" con el token adecuado y un project_id = 2
    Entonces obtengo status 404
    Y obtengo el cuerpo:
        "status": "The project requested could not be found",
        "message": "You have requested this URI [/users/1/favorites] but did you mean /users/<int:user_id>/favorites or /v1//users/<int:user_id>/favorites or /users/<int:user_id>/projects ?"
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body_usuario = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "hola"
    }
    client.post(
        "/users",
        data=json.dumps(body_usuario),
        content_type="application/json"
    )

    body_post = {
        "token": UserDBModel.encode_auth_token(1),
        "project_id": 1
    }
    client.post("/users/1/favorites",
                data=json.dumps(body_post),
                content_type="application/json")

    body_delete = {
        "token": UserDBModel.encode_auth_token(1),
        "project_id": 2,
    }
    delete_response = client.delete("/users/1/favorites",
                                    data=json.dumps(body_delete),
                                    content_type="application/json")

    assert delete_response is not None
    assert delete_response.status_code == 404
    user = json.loads(delete_response.data.decode())
    assert user['status'] == "The project requested could not be found"


def test_dada_una_db_con_usuario_de_id_1_con_un_proyecto_favorito_de_id_1_al_hacer_un_delete_de_un_proyecto_sin_mandar_project_id_se_obtiene_missing_arguments(test_app,
                                                                                                                                                               test_database):
    """
    Dada una base de datos con un usuario
    Cuando Delete "seers/1" con el token adecuado y sin un project_id
    Entonces obtengo status 404
    Y obtengo el cuerpo:
        "status" == "missing_args"
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body_usuario = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "hola"
    }
    client.post(
        "/users",
        data=json.dumps(body_usuario),
        content_type="application/json"
    )

    body_post = {
        "token": UserDBModel.encode_auth_token(1),
        "project_id": 1
    }
    client.post("/users/1/favorites",
                data=json.dumps(body_post),
                content_type="application/json")

    body_delete = {
        "token": UserDBModel.encode_auth_token(1)
    }
    delete_response = client.delete("/users/1/favorites",
                                    data=json.dumps(body_delete),
                                    content_type="application/json")

    assert delete_response is not None
    assert delete_response.status_code == 404
    user = json.loads(delete_response.data.decode())
    assert user['status'] == "missing_args"


def est_dada_una_db_con_usuario_de_id_1_con_un_proyecto_favorito_de_id_1_al_hacer_un_delete_de_un_proyecto_con_token_incorrecto_se_obtiene_user_not_found(test_app,
                                                                                                                                                          test_database):
    """
    Dada una base de datos con un usuario
    Cuando Delete "seers/1" con el token incorrecto y un project_id = 1
    Entonces obtengo status 404
    Y obtengo el cuerpo:
        "status" == "user_not_found"
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body_usuario = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "hola"
    }
    client.post(
        "/users",
        data=json.dumps(body_usuario),
        content_type="application/json"
    )

    body_post = {
        "token": UserDBModel.encode_auth_token(1),
        "project_id": 1
    }
    client.post("/users/1/favorites",
                data=json.dumps(body_post),
                content_type="application/json")

    body_delete = {
        "token": "",
        "project_id": 1,
    }
    delete_response = client.delete("/users/1/favorites",
                                    data=json.dumps(body_delete),
                                    content_type="application/json")

    assert delete_response is not None
    assert delete_response.status_code == 404
    assert delete_response['status'] == "Invalid token => Login again."
