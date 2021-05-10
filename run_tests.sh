#!/bin/sh
echo "[RUN_TESTS] waiting for postgres to start ..."
docker-compose exec service_users_web bash -c 'while ! nc -z service_users_db 5432; do sleep 1; done;'

echo "[RUN_TESTS] Running tests ..."
docker-compose exec service_users_web pytest "backend_users/tests" --cov="backend_users"

echo "[RUN_TESTS] Running flake8 inside all folders"
docker-compose exec service_users_web flake8 backend_users
