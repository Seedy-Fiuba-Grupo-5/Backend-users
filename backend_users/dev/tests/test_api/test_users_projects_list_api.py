import json
from prod.db_models.user_db_model import UserDBModel, UserProjectDBModel
from dev.aux_test import recreate_db

"""
def test_get_a_url_user_barra_id_1_barra_projects_devuelve_proyectos_asociados_al_usuario_de_id_1(
        test_app,
        test_database):
"""
"""
Dado una base de datos
Y un proyecto registrado:
    user_id = 1
    project_id = 1
Cuando GET "/users/1/projects"
Entonces obtengo status 200
Y obtengo 1 elemento con cuerpo:
{
    user_id = 1
    project_id = [1]
}
"""
"""
    session = recreate_db(test_database)
    client = test_app.test_client()
    body_register = {
        "name": "un nombre",
        "lastName": "un apellido",
        "email": "un email",
        "password": "una password"
    }
    response_register = client.post(
        "/users",
        data=json.dumps(body_register),
        content_type="application/json"
    )
    user_id = response_register['id']
    body_project = {
        "user_id": user_id,
        "project_id": 1
    }
    client.post(
        "/users/{}/projects".format(user_id),
        data=json.dumps(body_register),
        content_type="application/json"
    )
    response = client.get("/users/{}/projects".format(user_id))
    assert response is not None
    assert response.status_code == 200
    body = json.loads(response.data.decode())
    assert body['user_id'] == user_id
    id_projects_list = body['project_id']
    assert len(id_projects_list) == 1
    assert id_projects_list[0] == 1
"""

def test_get_a_url_user_barra_id_1_barra_projects_devuelve_el_usuario_sin_proyectos_cuando_el_usuario_no_existe(
        test_app,
        test_database):
    """
    Dado una base de datos vacia
    Cuando GET "/users/1/projects"
    Entonces obtengo status 200
    Y obtengo el cuerpo:
    {
        "user_id": 1,
        "project_id" : []
    }
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    user_id = 1
    response = client.get("/users/{}/projects".format(user_id))
    assert response is not None
    assert response.status_code == 200
    body = json.loads(response.data.decode())
    assert body['user_id'] == user_id
    id_projects_list = body['project_id']
    assert len(id_projects_list) == 0

