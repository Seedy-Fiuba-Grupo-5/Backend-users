import json
from backend_users.db_models.user_db_model import UserDBModel


def test_db_has_the_only_user_name_Franco_Martin_last_name_Di_Maria_and_fiuba_mail_fdimaria_GET_users_should_return_json_with_that_with_id_1(test_app, test_database):
    session = test_database.session
    session.add(UserDBModel(name="Franco Martin",
                            last_name="Di Maria",
                            email="fdimaria@fi.uba.ar"))
    session.commit()
    client = test_app.test_client()
    response = client.get("/users")
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert len(data) == 1
    user = data[0]
    assert user["id"] == 1
    assert user["name"] == "Franco Martin"
    assert user["last_name"] == "Di Maria"
    assert user["email"] == "fdimaria@fi.uba.ar"
