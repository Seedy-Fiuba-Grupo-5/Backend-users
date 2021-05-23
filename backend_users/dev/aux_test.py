def recreate_db(test_database):
    session = test_database.session
    session.remove()
    test_database.drop_all()
    test_database.create_all()
    return session
