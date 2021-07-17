# Dockerfile para produccion

# Imagen base de python
FROM python:3.8

# Directorio de trabajo
WORKDIR /usr/src/app

# Actualizar repositorios de apt
RUN apt-get update

# Copy Datadog configuration
COPY datadog-config/ /etc/datadog-agent/

# Install GPG dependencies
RUN apt-get install -y gpg apt-transport-https gpg-agent curl ca-certificates

# Add Datadog repository and signing keys
ENV DATADOG_APT_KEYRING="/usr/share/keyrings/datadog-archive-keyring.gpg"
ENV DATADOG_APT_KEYS_URL="https://keys.datadoghq.com"
RUN sh -c "echo 'deb [signed-by=${DATADOG_APT_KEYRING}] https://apt.datadoghq.com/ stable 7' > /etc/apt/sources.list.d/datadog.list"
RUN touch ${DATADOG_APT_KEYRING}
RUN curl -o /tmp/DATADOG_APT_KEY_CURRENT.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_CURRENT.public" && \
    gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_CURRENT.public
RUN curl -o /tmp/DATADOG_APT_KEY_F14F620E.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_F14F620E.public" && \
    gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_F14F620E.public
RUN curl -o /tmp/DATADOG_APT_KEY_382E94DE.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_382E94DE.public" && \
    gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_382E94DE.public

# Install the Datadog Agent
RUN apt-get update && apt-get -y --force-yes install --reinstall datadog-agent

# Expose DogStatsD and trace-agent ports
EXPOSE 8125/udp 8126/tcp
ENV DD_APM_ENABLED=true

# Instalar cliente Postgres para poder esperar
# la inicializacion de la base de datos
RUN apt-get -y install postgresql-client

# Instalar dependencias
RUN pip install --upgrade pip
COPY ./requirements-prod.txt /usr/src/app/requirements-prod.txt
RUN pip install -Ur requirements-prod.txt

# Copiar archivos de produccion
COPY /backend_users/prod /usr/src/app/backend_users/prod

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

# Ejecutar el script entrypoint.sh
CMD ["sh", "/usr/src/app/backend_users/prod/docker-entrypoint-prod.sh"]
