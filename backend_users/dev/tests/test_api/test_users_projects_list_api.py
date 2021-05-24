import json
from prod.db_models.user_db_model import UserProjectDBModel
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
        user_id = 1
        project_id = 1
    """
    session = recreate_db(test_database)
    session.add(UserProjectDBModel( user_id=1,
                                    project_id=1))

    session.commit()
    client = test_app.test_client()
    response = client.get("/users/1/projects")
    assert response is not None
    assert response.status_code == 200
    projects_list = json.loads(response.data.decode())
    assert len(projects_list) == 1
    project = projects_list[0]
    assert project['user_id'] == 1
    assert project['project_id'] == 1
