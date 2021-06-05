import json
from prod.db_models.user_db_model import UserDBModel, UserProjectDBModel
from dev.aux_test import recreate_db


def test_get_a_url_user_barra_id_1_barra_projects_devuelve_proyectos_asociados_al_usuario_de_id_1(
        test_app,
        test_database):
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
    session = recreate_db(test_database)
    user_id = UserDBModel.add_user('un nombre',
                                   'un apellido',
                                   'un email',
                                   'una password')
    UserProjectDBModel.add_project_to_user_id(user_id, 1)
    client = test_app.test_client()
    response = client.get("/users/{}/projects".format(user_id))
    assert response is not None
    assert response.status_code == 200
    body = json.loads(response.data.decode())
    assert body['user_id'] == user_id
    id_projects_list = body['project_id']
    assert len(id_projects_list) == 1
    assert id_projects_list[0] == 1


"""
def test_get_a_url_user_barra_id_1_barra_projects_devuelve_proyectos_asociados_al_usuario_de_id_1(
        test_app,
        test_database):

    # Dado una base de datos vacia
    # Cuando GET "/users/1/projects"
    # Entonces obtengo status 200
    # Y obtengo 0 elementos
    session = recreate_db(test_database)
    client = test_app.test_client()
    response = client.get("/users/1/projects")
    assert response is not None
    assert response.status_code == 200
    body = json.loads(response.data.decode())
    
    assert len(projects_list) == 0
"""
