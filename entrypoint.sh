#!/bin/sh

echo "Waiting for postgres..."

while !</dev/tcp/db/5432; do sleep 1; done;

echo "PostgreSQL started"

flask run --host=0.0.0.0 --port=${PORT:-5000}
