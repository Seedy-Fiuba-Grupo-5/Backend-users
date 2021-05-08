import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instanciar la base de datos
db = SQLAlchemy()

# App 'Factory'


def create_app(script_info=None):

    # Instanciar la aplicacion
    app = Flask(__name__)

    # Configuracion
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # Enlazar la base de datos
    db.init_app(app)

    # Registrar 'blueprints'
    # TODO: Utilizar el siguiente loop adaptandolo:
    """
    for name in ('users'):
    bp = import_string('api.{0}'.format(name))
    app.register_blueprint(bp, prefix='/{0}'.format(name))

    """

    import_blueprints(app)

    # TODO: Revisar si lo siguiente es necesario
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
    from .api.ping_v1_api import ping_v1_api
    app.register_blueprint(ping_v1_api)
    from .api.index_v1_api import index_v1_api
    app.register_blueprint(index_v1_api)
    from .api.users_v1_api import users_v1_api
    app.register_blueprint(users_v1_api)
