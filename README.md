# Seedy Fiuba Backend-Users
[![Backend-Users main](https://github.com/Seedy-Fiuba-Grupo-5/Backend-users/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Seedy-Fiuba-Grupo-5/Backend-users/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Seedy-Fiuba-Grupo-5/Backend-users/branch/main/graph/badge.svg)](https://codecov.io/gh/Seedy-Fiuba-Grupo-5/Backend-users)

[![Backend-Users develop](https://github.com/Seedy-Fiuba-Grupo-5/Backend-users/actions/workflows/develop.yml/badge.svg?branch=development-backend-users)](https://github.com/Seedy-Fiuba-Grupo-5/Backend-users/actions/workflows/develop.yml)
[![codecov](https://codecov.io/gh/Seedy-Fiuba-Grupo-5/Backend-users/branch/develop/graph/badge.svg)](https://codecov.io/gh/Seedy-Fiuba-Grupo-5/Backend-users)

## Tecnologias
- Flask (framework del servicio web)
- Postgres (Base de datos)

# Pruebas: pytest & flake8
pytest: libreria de python para 'testing'.  
pytest-cov: plugin de pytest para medir porcentaje de cobertura de las pruebas.  
flake8: 'linter' de python, basado en los lineamientos de pep8.  
  
1) Levantar los servicios:
```
docker-compose up -d --build --remove-orphans
```
Nota: Si no utilizan el flag '-d', podran ver los logs de los servicios en 
ejecucion.  
  
2) Pytest + Flake8:
```
./run_tests.sh
```
Nota 1: Este script requiere que los servicios se encuetren levantados.  
Nota 2: Este script esperara hasta que la base de datos se haya inicializado.  
  
3) Se pueden realizar cambios en el codigo y los servicios (en ejecucion), los detectaran y se actualizaran, permaneciendo en ejecucion.  
  
4) Una vez terminado de realizar testear la aplicacion y corregir todos los errores, se recomiendo detener los servicios:  
```
docker-compose stop
```
  
5) Para eliminar los servicios y toda la informacion que mantienen, ejecutar:
```
docker-compose down -v
```
  
## Autopep8
autopep8: Formatea el codigo de python para que se adecuado a los
lineamientos de pep8.  
Ejecutar el siguiente comando para auto-formatear el codigo.
```
./run_autopep8.sh
```
Nota: Los servicios deben estar levantados.  
  
# Entorno Heroku
## Informacion
Nombre de la aplicacion Heroku (App): seedy-fiuba-backend-users
Nombre del repositorio Heroku: https://git.heroku.com/seedy-fiuba-backend-users.git  
  
Heroku Postgres (BDD): postgresql-deep-68602  
(La aplicación desplegada en Heroku utiliza una base de datos Postgres propia de 
la plataforma, agregada como add-on de la aplicacion)  
  
URL de la aplicacion: https://seedy-fiuba-backend-users.herokuapp.com/  

## Despliegue
Nota: Los siguientes comandos no han sido probados para usuarios que no han creado el respositorio de Heroku.  
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
heroku container:push web
```
  
Ejecutar la imagen subida en la instancia de heroku
```
heroku
```

## Prendido y apagado del servicio
Prendido del servicio :
```
heroku ps:scale web=1
```

Apagado del servicio :
Atencion: En la implementacion actual, al apagar el servicio los datos que se encuentran en la base de datos se perderan.
```
heroku ps:scale web=0
```


# Entorno Local
## Docker-Compose
(Re-) Ejecutar las imagenes de los servicios web y db, 
y previamente construirlas: 
```
docker-compose up -d --build
```
web : Servidor web  
db : Base de datos Postgres local  

Destruir todas las imagenes:
```
docker-composer down -v
```
