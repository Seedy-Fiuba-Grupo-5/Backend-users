from prod.db_models.messages_db_model import MessagesDBModel
from dev.aux_test import recreate_db


def test_get_messages_form_user_1_to_user_2(test_app,
                                        test_database):
    """Este tests muestra como se obtienen los mensajes entre dos usuarios
    """
    session = recreate_db(test_database)
    session.add(MessagesDBModel(id_1=1,
                                id_2=2,
                                text="fdimaria@fi.uba.ar",
                                owner=1))
    session.commit()
    session.add(MessagesDBModel(id_1=1,
                                id_2=2,
                                text="fdimaria@fi.uba.ar",
                                owner=2))
    session.commit()
    messages = MessagesDBModel.get_messages_between_users(1,
                                                            2)
    assert len(messages) == 2


def test_get_messages_form_user_1_to_user_2_and_user_2_to_user_1(test_app,
                                                                 test_database):
    """Este tests prueba que se puedan obtener los mensajes asociados a los
    dos users independientemente de que usuario es el dueño del mensaje
    """
    session = recreate_db(test_database)
    session.add(MessagesDBModel(id_1=1,
                                id_2=2,
                                text="fdimaria@fi.uba.ar",
                                owner=1))
    session.commit()
    session.add(MessagesDBModel(id_1=2,
                                id_2=1,
                                text="fdimaria@fi.uba.ar",
                                owner=2))
    session.commit()
    messages = MessagesDBModel.get_messages_between_users(1,
                                                          2)
    assert len(messages) == 2
