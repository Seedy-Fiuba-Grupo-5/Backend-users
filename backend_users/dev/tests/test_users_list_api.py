import json
from prod.db_models.user_db_model import UserDBModel
from dev.aux_test import recreate_db


def test_db_has_the_only_user_name_Franco_Martin_last_name_Di_Maria_and_fiuba_mail_fdimaria_GET_users_should_return_json_with_that_with_id_1(
        test_app, test_database):
    session = test_database.session
    session.remove()
    test_database.drop_all()
    test_database.create_all()
    session.add(UserDBModel(name="Franco Martin",
                            lastname="Di Maria",
                            email="fdimaria@fi.uba.ar",
                            password="hola"))
    session.commit()
    client = test_app.test_client()
    response = client.get("/users")
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert len(data) == 1
    user = data[0]
    assert user["id"] == 1
    assert user["name"] == "Franco Martin"
    assert user["lastName"] == "Di Maria"
    assert user["email"] == "fdimaria@fi.uba.ar"


def test_db_has_the_users_user1_name_Franco_Martin_last_name_Di_Maria_and_fiuba_mail_fdimaria_user2_name_Brian_last_name_Zambelli_Tello_and_fiuba_mail_bzambelli_GET_users_should_return_json_with_that_ids_1_2(
        test_app, test_database):
    session = test_database.session
    session.remove()
    test_database.drop_all()
    test_database.create_all()
    session.add(UserDBModel(name="Franco Martin",
                            lastname="Di Maria",
                            email="fdimaria@fi.uba.ar",
                            password="hola"))
    session.add(UserDBModel(name="Brian",
                            lastname="Zambelli Tello",
                            email="bzambelli@fi.uba.ar",
                            password="hola"))
    session.commit()
    client = test_app.test_client()
    response = client.get("/users")
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert len(data) == 2
    user_franco = data[0]
    user_brian = data[1]
    assert user_franco["id"] == 1
    assert user_franco["name"] == "Franco Martin"
    assert user_franco["lastName"] == "Di Maria"
    assert user_franco["email"] == "fdimaria@fi.uba.ar"
    assert user_brian["id"] == 2
    assert user_brian["name"] == "Brian"
    assert user_brian["lastName"] == "Zambelli Tello"
    assert user_brian["email"] == "bzambelli@fi.uba.ar"


def test_db_vacia_post_users_name_franco_martin_last_name_di_maria_email_fdimaria_password_tomate_entonces_registra_nuevo_usuario_con_id_1(
        test_app,
        test_database):
    session = recreate_db(test_database)
    client = test_app.test_client()
    body = {
        "name": "Franco Martin",
        "lastName": "Di Maria",
        "email": "fdimaria@fi.uba.ar",
        "password": "tomate"
    }
    response = client.post(
        "/users",
        data=json.dumps(body),
        content_type="application/json",
    )
    """assert response.status_code == 201
    register_info = json.loads(response.data.decode())
    assert len(register_info) == 4
    assert register_info["name"] == "Franco Martin"
    assert register_info["lastName"] == "Di Maria"
    assert register_info["email"] == "fdimaria@fi.uba.ar"
    assert register_info["id"] == 1"""
