#!/bin/sh
  
until PGPASSWORD=$POSTGRES_PASSWORD psql $DATABASE_URL -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
  
>&2 echo "Postgres is up - executing command"

# Indica a Flask que levante un servidor
# 0.0.0.0 : El servidor sera publicamente visible
# ${PORT:-5001} : El puerto donde se bindea el server 
# esta especificado por la variable de entorno PORT.  
# PORT=5001, por defecto.
flask run --host=0.0.0.0 --port=${PORT:-5001}
