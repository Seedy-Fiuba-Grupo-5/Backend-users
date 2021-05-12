import os


class BaseConfig:
    """Configuracion base"""

    # TODO: Usar otra clave secreta
    SECRET_KEY = "my_precious"
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    """Configuracion para entorno de produccion"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("://", "ql://", 1)
