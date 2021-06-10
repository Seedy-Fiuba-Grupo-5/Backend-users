import json

from dev.aux_test import recreate_db
from prod.db_models.user_db_model import UserDBModel


def test_get_correct_encode_and_decode_of_id(test_app,
                                             test_database):
    """Este test muestra como se accede al endpoint asociado a la
    verificacion del token.
    Se agrega a un usuario y, luego, se intenta obtener el token asociado
    al id del mismo para verificar si es un usuario valido, o no, al
    momento de su chequeo."""
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
    response = client.post(
        'users/auth',
        data=json.dumps(body),
        content_type="application/json"
    )
    assert response.status_code == 200
    print(response)
