import json
from prod.db_models.admin_db_model import AdminDBModel
from prod.db_models.user_db_model import UserDBModel
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
    response = client.patch("/admins/users/1",data=json.dumps(body_2),
                            content_type="application/json")
    assert response.status_code == 200
