import json

from dev.aux_test import recreate_db
from prod.db_models.user_db_model import UserDBModel


def test_post_message(test_app,
                      test_database):
    """Este test muestra como se crea un mensaje asociado a la
    conversacion entre dos usuarios"""
    session = recreate_db(test_database)
    client = test_app.test_client()
    body = {
        "id_1": 1,
        "message": "Di Maria",
        "token": UserDBModel.encode_auth_token(1),
    }
    response = client.post(
        "/messages/2",
        data=json.dumps(body),
        content_type="application/json"
    )
    assert response.status_code == 201


def test_get_messages(test_app,
                      test_database):
    """Este test muestra como se obtienen los mensajes asociados a la
    conversacion entre dos usuarios"""
    session = recreate_db(test_database)
    client = test_app.test_client()
    body = {
        "id_1": 1,
        "message": "Di Maria",
        "token": UserDBModel.encode_auth_token(1),
    }
    response = client.post(
        "/messages/2",
        data=json.dumps(body),
        content_type="application/json"
    )
    assert response.status_code == 201
    body = {
        "id_1": 2,
        "message": "Di Maria",
        "token": UserDBModel.encode_auth_token(2),
    }
    response = client.post(
        "/messages/1",
        data=json.dumps(body),
        content_type="application/json"
    )
    assert response.status_code == 201
    body = {
        "token": UserDBModel.encode_auth_token(2),
    }
    response = client.get(
        "/messages/2",
        data=json.dumps(body),
        content_type="application/json"
    )
    assert response.status_code == 200
    patch_data = json.loads(response.data.decode())
    assert len(patch_data) == 2
    body = {
        "token": UserDBModel.encode_auth_token(1),
    }
    response = client.get(
        "/messages/1",
        data=json.dumps(body),
        content_type="application/json"
    )
    assert response.status_code == 200
    patch_data = json.loads(response.data.decode())
    assert len(patch_data) == 2
