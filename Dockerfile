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

# Indica a Flask en que modulo se encuetra la aplicacion
ENV FLASK_APP=manage

# Instalar netcat para script de espera de postgres
RUN apt-get update && apt-get install -y netcat

# Instalar dependencias
RUN pip install --upgrade pip
COPY ./requirements-prod.txt /usr/src/app/requirements-prod.txt
RUN pip install -Ur requirements-prod.txt

# Copiar archivos de proyecto al directorio de trabajo
COPY . /usr/src/app/

# Indica a Flask que levante un servidor
# 0.0.0.0 : El servidor sera publicamente visible
# ${PORT:-5000} : El puerto donde se bindea el server 
# esta especificado por la variable de entorno PORT.  
# PORT=5000, por defecto.
CMD flask run --host=0.0.0.0 --port=${PORT:-5000}
