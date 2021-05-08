import os


class BaseConfig:
    """Configuracion base"""

    # TODO: Usar otra clave secreta
    SECRET_KEY = "my_precious"
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Configuracion para entorno de desarrollo"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestingConfig(BaseConfig):
    """Configuracion para entorno de pruebas"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")


class ProductionConfig(BaseConfig):
    """Configuracion para entorno de produccion"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
