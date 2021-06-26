import json
from prod.db_models.user_db_model import UserDBModel, UserProjectDBModel
from dev.aux_test import recreate_db

PARCIAL_URL = "/projects"


def test_get_project_id_retorna_error_cuando_el_project_no_existe(
    test_app,
    test_database
):
    """
    Dada una base de datos vacia.
    Cuando GET /projects/<id>
    Entonces obtengo 404
    Con cuerpo:
        "status": "The project requested could not be found"
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    project_id = 333
    url = PARCIAL_URL + "/" + str(project_id)
    res = client.get(url)
    assert res.status_code == 404
    body = json.loads(res.data.decode())
    assert body['status'] == "The project requested could not be found"


def test_get_project_id_retorna_info_del_proyecto_cuando_existe(
    test_app,
    test_database
):
    """
    Dada una base de datos.
    Con usuario registrado:
        'id': '<user_id>'
    Y un proyecto asociado a dicho usuario:
        'project_id': '3'
    Cuando GET /projects/<id>
    Entonces obtengo 200
    Con cuerpo:
        "project_id" : <int:project_id>
        "user_id": <int:user_id>
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    body = {
        'name': 'a name',
        'lastName': 'a last name',
        'email': 'name@lastname.com',
        'password': 'a password'
    }
    res = client.post('/users', json=body)
    data = json.loads(res.data.decode())
    user_id = data['id']

    project_id = 3
    body = {'project_id': project_id}
    url = '/users' + '/' + str(user_id) + '/projects'
    res = client.post(url, json=body)

    url = PARCIAL_URL + '/' + str(project_id)
    res = client.get(url)
    assert res.status_code == 200
    data = json.loads(res.data.decode())
    assert data['project_id'] == project_id
    assert data['user_id'] == user_id
