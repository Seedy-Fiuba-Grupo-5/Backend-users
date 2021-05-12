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
ENV FLASK_APP=backend_users/prod/manage

# Indica a Flask en que modulo se encuetra la configuracion de 
# la aplicacion
ENV APP_SETTINGS=src.config.ProductionConfig

# Instalar netcat para script de espera de postgres
RUN apt-get update && apt-get install -y netcat

# Instalar dependencias
RUN pip install --upgrade pip
COPY ./requirements-prod.txt /usr/src/app/requirements-prod.txt
RUN pip install -Ur requirements-prod.txt

# Copiar archivos de produccion
COPY /backend_users/src /usr/src/app/backend_users/src

# Indica a Flask que levante un servidor
# 0.0.0.0 : El servidor sera publicamente visible
# ${PORT:-5000} : El puerto donde se bindea el server 
# esta especificado por la variable de entorno PORT.  
# PORT=5000, por defecto.
CMD flask run --host=0.0.0.0 --port=${PORT:-5000}
