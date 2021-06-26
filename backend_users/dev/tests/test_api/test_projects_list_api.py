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
