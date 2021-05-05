#!/bin/sh
echo "Running web ..."

python manage.py run -h 0.0.0.0

echo "Creating db ..."

exec web python manage.py create_db
