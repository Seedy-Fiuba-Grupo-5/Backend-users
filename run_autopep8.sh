#!/bin/sh
echo "[RUN AUTOPEP8] Running autopep8 inside all folders ..."
docker-compose exec service_users_web autopep8 --in-place --recursive .
