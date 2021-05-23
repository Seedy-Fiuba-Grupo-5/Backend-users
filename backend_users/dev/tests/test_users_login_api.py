import json
from prod.db_models.user_db_model import UserDBModel
from dev.aux_test import recreate_db
def test_dado_email_fdimaria_registrado_con_id_1_y_palabra_de_pase_tomate_cuando_POST_a_url_users_barra_login_el_email_y_la_palabra_de_pase_obtengo_el_email_y_el_id_anterior(test_app, test_database):
    session = recreate_db(test_database)
    session.add(UserDBModel(name="Franco Martin",
                            lastname="Di Maria",
                            email="fdimaria@fi.uba.ar",
                            password="tomate"))
    session.commit()
    client = test_app.test_client()
    body = {
        "email": "fdimaria@fi.uba.ar", 
        "password" : "tomate"
        }
    response = client.post(
        "/users/login",
        data=json.dumps(body),
        content_type="application/json",
    )
    login_info = json.loads(response.data.decode())
    assert response.status_code == 200
    assert login_info["id"] == 1
    assert login_info["email"] == "fdimaria@fi.uba.ar"
