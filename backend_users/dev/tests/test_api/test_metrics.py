import json

from dev.aux_test import recreate_db
from prod.db_models.user_db_model import UserDBModel


def test_get_correct_metrics(test_app, test_database):
    """Este test muestra como se generan y obtienen metricas usando  l
    endpoint asociado."""
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
    body = {"token": UserDBModel.encode_auth_token(1)}
    client.post(
        'users/auth',
        data=json.dumps(body),
        content_type="application/json"
    )
    response = client.get('users/metrics',
                           data=json.dumps(body),
                           content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["percentage_blocked"] == 0

def test_metric_percentage_blocked(test_app, test_database):
    """En este test, se va a probar que el valor retornado en cuanto
    a usuarios bloqueados, es correcto"""
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
    body = {"token": UserDBModel.encode_auth_token(1)}
    client.post(
        'users/auth',
        data=json.dumps(body),
        content_type="application/json"
    )
    response = client.get('users/metrics',
                          data=json.dumps(body),
                          content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["percentage_blocked"] == 0
    UserDBModel.flip_active_status(1)
    response = client.get('users/metrics',
                          data=json.dumps(body),
                          content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data["percentage_blocked"] == 1

