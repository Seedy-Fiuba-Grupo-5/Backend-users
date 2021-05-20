import json
from prod.db_models.user_db_model import UserProjectDBModel


def test_devuelve_los_proyectos_asociados_a_un_usuario_cuando_la_relacion_usuario_pass_es_correcta(
        test_app,
        test_database):
    session = test_database.session
    session.remove()
    test_database.drop_all()
    test_database.create_all()
    session.add(UserProjectDBModel(user_id=1,
                                   project_id=1))

    session.commit()
    client = test_app.test_client()
    response = client.get("/users/projects/1")
    assert response is not None
    assert response.status_code == 200
