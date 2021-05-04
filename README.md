# shiny-docker
Pruebas sobre bdd-flask-heroku
Para instalar Docker ejecutar el siguiente comando:
```sudo apt  install docker-compose```

Hay que ejecutar los comandos de docker dentro de la carpeta correspondiente (puede ser necesário agregar ```sudo```)

```docker-compose up -d --build```

```docker-compose exec web python manage.py create_db```

```docker-compose exec web python manage.py seed_db```
