#!/bin/sh
echo "[RUN AUTOPEP8] Starting services ..."
docker-compose up -d --build
echo "[RUN AUTOPEP8] Running autopep8 inside all folders ..."
docker-compose exec service_users_web autopep8 --in-place --recursive .
echo "[RUN AUTOPEP8] Turning down services ..."
docker-compose down -v
