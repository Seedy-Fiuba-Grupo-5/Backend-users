import os
from prod.config import BaseConfig


class DevelopmentConfig(BaseConfig):
    """Configuracion para entorno de desarrollo"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestingConfig(BaseConfig):
    """Configuracion para entorno de pruebas"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
