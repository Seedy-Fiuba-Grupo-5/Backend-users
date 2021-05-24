import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instanciar la base de datos
db = SQLAlchemy()


def create_app(script_info=None):
    # App 'Factory'

    # Instanciar la aplicacion
    app = Flask(__name__)

    # Configuracion
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # Enlazar la base de datos
    db.init_app(app)

    import_blueprints(app)

    # Contexto de la 'shell' para flask cli
    # Registra las instancias app y db en la 'shell'.
    # Permite trabajar con el contexto de la aplicacion
    # y la base de datos sin tener que importarlos
    # directamente en la 'shell'
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app


def import_blueprints(app):
    # /users
    from .api.users_list_api import users_list_api
    app.register_blueprint(users_list_api)

    # /users/<user_id>
    from .api.one_user_api import one_user_api
    app.register_blueprint(one_user_api)

    # /users/login
    from .api.users_login_api import users_login_api
    app.register_blueprint(users_login_api)

    # /users/projects/<user_id>
    from .api.projects_from_user_api import users_list_projects_api
    app.register_blueprint(users_list_projects_api)
