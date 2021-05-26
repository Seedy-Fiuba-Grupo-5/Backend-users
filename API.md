# API del servicio

## users/
### POST 
#### Cuerpo del mensaje (body)
{
  "name" : String,
  "lastName" : String,
  "email" : String,
  "password" : String,
}
#### Respuesta
##### 201 (status code)
{
  "name" : String,
  "lastName" : String,
  "email" : String,
  "id": Int
}

##### 401 (status code)
'Ya existe un usuario registrado para el mail recibido'

##### 400 (status code)
'Faltan campos en la solicitud'

## users/login
### POST
#### Cuerpo del mensaje (body)
{
  "email": String,
  "password": String
}
#### Respuesta
##### 200 (status code)
{
  "email": String,
  "id": Int
}

##### 401 (status code)
'Ya existe un usuario registrado para el mail recibido'

##### 400 (status code)
'Faltan contraseña y/o password'


