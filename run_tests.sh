docker-compose up -d --build --remove-orphans
docker exec seedy_users_web python -m pytest
docker-compose down