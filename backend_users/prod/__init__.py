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

    # Importar extensiones
    import_blueprints(app)

    return app


def import_blueprints(app):
    # /users/projects/<user_id>
    from .api.users_projects_list_api import users_projects_list_api
    app.register_blueprint(users_projects_list_api)

    # API
    from .api import api_bp
    app.register_blueprint(api_bp)
