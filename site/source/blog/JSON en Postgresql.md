Title: JSON en PostgreSQL
Date: 2021-03-15
Tags: postgresql
Slug: json-postgresql
Author: __alexander__
Summary: PostgreSQL incluye soporte para el tipo de dato JSON desde la versión "9.2". En este tutorial se verán ejemplos de cómo trabajar con inserciones y consultas de campos JSON.

PostgreSQL incluye soporte para el tipo de dato JSON desde la versión "9.2". En este tutorial se verán ejemplos de cómo trabajar con inserciones y consultas de campos JSON.

## ¿Qué es JSON?

JSON, es el acrónimo de "JavaScript Object Notation" o "notación de objeto de JavaScript". Es un formato de texto sencillo utilizado para el intercambio de datos.

Su estructura es similar a la del siguiente ejemplo:

~~~
::javascript
{
  "autor": "Isaac Asimov",
  "pais": "Rusia",   
  "libros":[
    {
      "titulo": "Yo robot",
      "isbn": "9780739312698"
    },{
      "nombre": "El hombre bicentenario",
      "isbn": "9788440677778"
    } 
  ]
}
~~~

## Creación de una tabla que utiliza un campo de tipo JSON

La declaración de una columna JSON solo requiere el nombre del campo + el tipo de dato "json", por ejemplo:

~~~
::sql
CREATE TABLE book (
   id serial,
   info json
);
~~~

En la tabla anterior almacenaremos información sobre grupos de libros por autores.

## Inserción de registros

~~~
::sql
INSERT INTO book (info)
	VALUES ('{"autor": "Isaac Asimov","pais": "Rusia","libros":[{"titulo": "Yo robot","isbn": "9780739312698"}]}');
~~~

o para insertar varios registros al mismo tiempo:

~~~
::sql
INSERT INTO book (info)
	VALUES ('{"autor": "Patrick Rothfuss","pais": "EEUU","libros":[{"titulo": "El nombre del viento","isbn": "9788499082479"}]}'),
    ('{"autor": "Arthur C. Clarke","pais": "Reino Unido","libros":[{"titulo": "Cánticos de la lejana Tierra","isbn": "9788401322013"}]}');
~~~

##  Consultas

Para ver la información que ya tenemos almacenada podemos usar:

~~~
::sql
SELECT id, info FROM book;
~~~

y para mostrar un atributo del json, podemos utilizar el operador "->":

~~~
::sql
SELECT info->'autor' FROM book;
~~~

| autor (json)  | 
| -----------   |
| "Isaac Asimov"       |
| "Patrick Rothfuss"   |
| "Arthur C. Clarke"   |

Noten que el operador nos retorna un tipo "json", pero si utilizamos la versión "->>" se transforma en un tipo "text":

~~~
::sql
SELECT info->>'autor' as autor, info->'pais' as pais FROM book;
~~~

| autor (text)  | pais (json) | 
| -----------   | ----------- |
| Isaac Asimov      |   "Rusia" |
| Patrick Rothfuss  |   "EEUU" |
| Arthur C. Clarke  |   "Reino Unido" |

## Consultas con condicionales (WHERE)

Por ejemplo, si deseamos obtener los registros cuyos autores pertenezcan a un país, podemos realizar una consulta similar a:

~~~
::sql
SELECT info FROM book WHERE info->>'pais' = 'Rusia';
~~~

Nótese que para comparar un valor del json con un "text" debemos utilizar el operador: "->>".

- - -

Se pueden realizar consultas y operaciones más complejas, pero como al menos como introducción, espero que este post les haya sido de ayuda.

## Referencias

* <a href="https://www.postgresql.org/docs/12/datatype-json.html" target="_blank">JSON Datatype</a>
* <a href="https://www.postgresql.org/docs/12/functions-json.html" target="_blank">JSON Functions and Operators</a>
