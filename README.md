# Servicio Web: Usuarios de SeedyFIUBA
- Flask (framework del servicio web)
- Postgres (Base de datos)

## Entorno Heroku
### Informacion
Nombre de la aplicacion Heroku (App): shrouded-meadow-59625  
Nombre del repositorio Heroku: https://git.heroku.com/shrouded-meadow-59625.git  
  
Heroku Postgres (BDD): postgresql-deep-68602  
(La aplicación desplegada en Heroku utiliza una base de datos Postgres propia de 
la plataforma, agregada como add-on de la aplicacion)  
  
URL de la aplicacion: https://shrouded-meadow-59625.herokuapp.com/  


# Despliegue
Nota: Los siguientes comandos no han sido probados para usuarios que no han creado el respositorio de Heroku.  
Conectarse a Heroku:
```
heroku login
```
  
Agregar repositorio remoto de Heroku
```
heroku git:remote -a shrouded-meadow-59625
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

### Prendido y apagado del servicio
Prendido del servicio :
```
heroku ps:scale web=1
```

Apagado del servicio :
Atencion: En la implementacion actual, al apagar el servicio los datos que se encuentran en la base de datos se perderan.
```
heroku ps:scale web=0
```


## Entorno Local
### Docker-Compose
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