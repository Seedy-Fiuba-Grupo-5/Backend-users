#!/bin/sh
docker-compose up -d --build
docker-compose exec service_users_web pytest "backend_users/tests" -p no:warnings --cov="backend_users"
docker-compose exec service_users_web flake8 backend_users
docker-compose down -v
