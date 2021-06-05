# Seedy Fiuba Backend-Users
[![Main](https://github.com/Seedy-Fiuba-Grupo-5/Backend-users/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Seedy-Fiuba-Grupo-5/Backend-users/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Seedy-Fiuba-Grupo-5/Backend-users/branch/main/graph/badge.svg)](https://codecov.io/gh/Seedy-Fiuba-Grupo-5/Backend-users/branch/main)

[![Develop](https://github.com/Seedy-Fiuba-Grupo-5/Backend-users/actions/workflows/develop.yml/badge.svg?branch=develop)](https://github.com/Seedy-Fiuba-Grupo-5/Backend-users/actions/workflows/develop.yml)
[![codecov](https://codecov.io/gh/Seedy-Fiuba-Grupo-5/Backend-users/branch/develop/graph/badge.svg)](https://codecov.io/gh/Seedy-Fiuba-Grupo-5/Backend-users/branch/develop)

# Seedy Fiuba Backend-Users
[![Main](https://github.com/Seedy-Fiuba-Grupo-5/Backend-users/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Seedy-Fiuba-Grupo-5/Backend-users/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Seedy-Fiuba-Grupo-5/Backend-users/branch/main/graph/badge.svg)](https://codecov.io/gh/Seedy-Fiuba-Grupo-5/Backend-users/branch/main)

[![Develop](https://github.com/Seedy-Fiuba-Grupo-5/Backend-users/actions/workflows/develop.yml/badge.svg?branch=develop)](https://github.com/Seedy-Fiuba-Grupo-5/Backend-users/actions/workflows/develop.yml)
[![codecov](https://codecov.io/gh/Seedy-Fiuba-Grupo-5/Backend-users/branch/develop/graph/badge.svg)](https://codecov.io/gh/Seedy-Fiuba-Grupo-5/Backend-users/branch/develop)

## Tecnologias
- Flask (framework del servicio web)
- Postgres (base de datos)
- JWT (tokens de accesso)

## Entorno Local

### Construccion
```
docker-compose build --remove-orphans
```

### Levantar servicios
```
docker-compose up
```

### Pruebas: pytest & flake8
pytest: libreria de python para 'testing'.  
pytest-cov: plugin de pytest para medir porcentaje de cobertura de las pruebas.  
flake8: 'linter' de python, basado en los lineamientos de pep8.  
  
2) Pytest + Flake8:
```
./run_tests.sh
```
Nota 1: Este script requiere que los servicios se encuetren levantados.  
Nota 2: Este script esperara hasta que la base de datos se haya inicializado.  
  
3) Se pueden realizar cambios en el codigo y los servicios (en ejecucion), los detectaran y se actualizaran, permaneciendo en ejecucion.  

### Autopep8
autopep8: Formatea el codigo de python para que se adecuado a los
lineamientos de pep8.  
```
./run_autopep8.sh
```
Nota: Este script requiere que los servicios se encuetren levantados.  

### Postgres psql
```
docker exec -it -u postgres container_users_db psql
```

### Detener servicios  
```
docker-compose stop
```
Nota: Mantiene el estado de la base de datos.  

### Destruir contenedores
```
docker-compose down -v
```
  
## Entorno Heroku
## Informacion
Nombre de la aplicacion Heroku (App): seedy-fiuba-backend-projects
Nombre del repositorio Heroku: https://git.heroku.com/seedy-fiuba-backend-users.git  
  
Heroku Postgres (BDD): postgresql-deep-68602
(La aplicación desplegada en Heroku utiliza una base de datos Postgres propia de 
la plataforma, agregada como add-on de la aplicacion)  
  
URL de la aplicacion: https://seedy-fiuba-backend-users.herokuapp.com/  

## Despliegue
Conectarse a Heroku:
```
heroku login
```
  
Agregar repositorio remoto de Heroku
```
heroku git:remote -a seedy-fiuba-backend-users
```
Nota: El creador del repositorio de Heroku deberia hacer colaborado a quienes quieren pushear al mismo.  
  
Conectarse al contenedor de Heroku:
```
heroku container:login
```
  
Construir imagen de la aplicacion y pushear a heroku:
```
heroku container:push web --app seedy-fiuba-backend-users
```
  
Ejecutar la imagen subida en la instancia de heroku
```
heroku container:release web --app seedy-fiuba-backend-users
```

## Prendido y apagado del servicio
Prendido del servicio :
```
heroku ps:scale web=1 --app seedy-fiuba-backend-users
```

Apagado del servicio :
```
heroku ps:scale web=0 --app seedy-fiuba-backend-users
```

## Postgres psql
```
heroku pg:psql --app seedy-fiuba-backend-users
```

# Postgres 
## Recontruir toda la base de datos
```
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```