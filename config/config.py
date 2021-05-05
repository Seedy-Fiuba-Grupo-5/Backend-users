import os

basedir = os.path.abspath(os.path.dirname(__file__))


# Definicion de la clase Config, necesaria para la utilizacion de
# SQLALCHEMY
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
