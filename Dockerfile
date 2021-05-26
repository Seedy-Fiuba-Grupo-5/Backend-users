# Dockerfile para produccion

# Imagen base de python 
FROM python:3.8

# Directorio de trabajo
WORKDIR /usr/src/app

# Indica al inteprete de Python que no genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Indica a Python que su salida estandar se envie directamente 
# a la terminal, sin esperar en un buffer intermedio.
ENV PYTHONUNBUFFERED 1

# Indica a Flask que estamos en un ambiente de produccion
ENV FLASK_ENV=production

# Indica a Flask en que modulo se encuetra la aplicacion
ENV FLASK_APP=backend_users/prod/main

# Indica a Flask en que modulo se encuetra la configuracion de 
# la aplicacion
ENV APP_SETTINGS=prod.config.ProductionConfig

# Actualizar repositorios de apt
RUN apt-get update

# Instalar cliente Postgres para poder esperar 
# la inicializacion de la base de datos
RUN apt-get -y install postgresql-client

# Instalar dependencias
RUN pip install --upgrade pip
COPY ./requirements-prod.txt /usr/src/app/requirements-prod.txt
RUN pip install -Ur requirements-prod.txt

# Copiar archivos de produccion
COPY /backend_users/prod /usr/src/app/backend_users/prod

# Ejecutar el script entrypoint.sh
ENTRYPOINT ["sh", "/usr/src/app/backend_users/prod/entrypoint.sh"] 
