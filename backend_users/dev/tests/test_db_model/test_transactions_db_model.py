from prod.db_models.user_db_model import UserDBModel
from prod.db_models.transactions_db_model import TransactionsDBModel
from dev.aux_test import recreate_db
from prod.exceptions import InvalidTransitionType, InvalidTransitionAmount


def test_favoritesdbmodel_aniadir_transaccion_tipo_support_esta_se_agrega_correctamente(
        test_app,
        test_database):
    """
    Dada una base de datos vacia
    Cuando agrego una transaccion con tipo support esta se agrega correctamente
    """
    session = recreate_db(test_database)
    id_project_list = TransactionsDBModel.add_transaction(
        11, 22, 33, "support").serialize()
    assert id_project_list['transaction_id'] == 1
    assert id_project_list['user_id'] == 11
    assert id_project_list['project_id'] == 22
    assert id_project_list['amount'] == 33
    assert id_project_list['type'] == "support"


def test_favoritesdbmodel_aniadir_transaccion_tipo_pay_esta_se_agrega_correctamente(
        test_app,
        test_database):
    """
    Dada una base de datos vacia
    Cuando agrego una transaccion con tipo pay esta se agrega correctamente
    """
    session = recreate_db(test_database)
    id_project_list = TransactionsDBModel.add_transaction(
        11, 22, 33, "pay").serialize()
    assert id_project_list['transaction_id'] == 1
    assert id_project_list['user_id'] == 11
    assert id_project_list['project_id'] == 22
    assert id_project_list['amount'] == 33
    assert id_project_list['type'] == "pay"


def test_favoritesdbmodel_aniadir_transaccion_tipo_hola_esta_se_lanza_invalid_transaction_type(
        test_app,
        test_database):
    """
    Dada una base de datos vacia
    Cuando agrego una transaccion con tipo hola esta lanza una excepcion
    """
    session = recreate_db(test_database)
    try:
        id_project_list = TransactionsDBModel.add_transaction(
            11, 22, 33, "hola").serialize()
        assert id_project_list['transaction_id'] == 1
        assert id_project_list['user_id'] == 11
        assert id_project_list['project_id'] == 22
        assert id_project_list['amount'] == 33
        assert id_project_list['type'] == "hola"
        assert False
    except InvalidTransitionType:
        assert True


def test_favoritesdbmodel_aniadir_con_monto_negativo_esta_se_lanza_invalid_transaction_amount(
        test_app,
        test_database):
    """
    Dada una base de datos vacia
    Cuando agrego una transaccion con valor negativo, esta lanza una excepcion
    """
    session = recreate_db(test_database)
    try:
        id_project_list = TransactionsDBModel.add_transaction(
            11, 22, -33, "support").serialize()
        assert id_project_list['transaction_id'] == 1
        assert id_project_list['user_id'] == 11
        assert id_project_list['project_id'] == 22
        assert id_project_list['amount'] == -33
        assert id_project_list['type'] == "support"
        assert False
    except InvalidTransitionAmount:
        assert True
