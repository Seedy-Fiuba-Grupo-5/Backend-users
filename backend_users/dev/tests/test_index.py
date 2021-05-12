import json


def test_GET_index_should_return_API_documentation(test_app):
    client = test_app.test_client()
    response = client.get("/")
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data["GET /users"] == "status_code 200 =>" +\
        "[{id: <integer>, " +\
        "name: <string>, " +\
        "lastName: <string>, " +\
        "email: <string>, " +\
        "active: <boolean>}]"
