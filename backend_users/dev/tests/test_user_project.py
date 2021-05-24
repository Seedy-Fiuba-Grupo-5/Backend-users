from prod.db_models.user_db_model import UserProjectDBModel


def test_get_projects_associated_to_user(test_app,
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
