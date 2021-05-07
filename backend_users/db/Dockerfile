FROM postgres:12-alpine

# Agregagmos script para ejecutar tras iniciar postgres
ADD create.sql /docker-entrypoint-initdb.d
