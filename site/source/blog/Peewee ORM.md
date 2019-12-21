Title: Peewee: ORM para python - I
Date: 2019-12-20 22:00
Tags: python, base-de-datos, peewee,
Slug: peewee-orm-para-python-1
Author: __alexander__

##### ¿Qué es?

Peewee es un [ORM][ORM] para python. Incluye soporte para SQLite, MySQL, PostgreSQL y Cockroachdb.


##### ¿Qué es un ORM?

Sus siglas significan *Object-Relational mapping*, o en español: *Mapeo Objeto-relacional*. Es una técnica que permite convertir entre los tipos de datos usados en los lenguajes de programación orientados a objetos y los tipos de datos de algun sistema de base de datos relacional.


##### Instalación

Se instala mediante [pip][pip].

> pip install peewee

Para comprobar que se haya realizado la instalación, podemos acceder a la consola interactiva de python y escribimos:

~~~
::python

>>> import peewee
>>> peewee.__version__
3.13.1
~~~

puede consultar más información sobre la instalación [aquí][peewee-instalacion].

- - -

##### Ejemplo de uso

Para ilustrar[^1] la idea, utilizaremos el mismo ejemplo de un post anterior que realicé sobre [sqlalchemy](https://alexanderae.com/sqlalchemy-orm-para-python-1.html).

El ejemplo es sobre un modelo de datos para un sistema que se encarga de administrar registros de libros, autores, y etiquetas (o temas, para los libros).

El esquema del modelo es el siguiente:

![modelo-libros][modelo-libros]

Consiste en las tablas Libro, Autor y Etiqueta principalmente.
Las tablas intermediarias *etiqueta_libro* y *autor_libro* se utilizan para expresar la relación de *muchos a muchos* entre las otras tablas.

Primero, debemos mapear el modelo de la base de datos por medio de peewee, para lo cual escribí tenemos el archivo siguiente que nombrare *models.py*:


~~~
::python

import datetime

from peewee import *

db = SqliteDatabase('libros.db')


class Autor(Model):
    nombre = CharField(max_length=120)

    class Meta:
        database = db


class Etiqueta(Model):
    nombre = CharField(max_length=120)

    class Meta:
        database = db


class Libro(Model):
    titulo = CharField(max_length=120, index=True)
    fecha_publicacion = DateField(default=datetime.datetime.now)
    isbn = CharField(max_length=13, index=True, unique=True)
    autores = ManyToManyField(Autor, backref='libros')
    etiquetas = ManyToManyField(Etiqueta, backref='libros')

    class Meta:
        database = db


db.connect()
db.create_tables([Autor,
                  Etiqueta,
                  Libro,
                  Libro.autores.get_through_model(),
                  Libro.etiquetas.get_through_model()]
                 )
~~~

Lo que realiza el código anterior es lo siguiente:

1. Importa los módulos necesarios

2. Realiza la conexión a la base de datos, en este caso corresponde a sqlite

3. Mapeamos las tablas como clases, utilizando los tipos de datos de **peewee**.

4. Añadimos las relaciones entre las tablas por medio del campo *ManyToManyField*

5. Al final, usamos la sentencia:

        db.create_tables
        
    observando que para crear las tablas intermedias (libro_autor y libro_etiquetas) utilizamos una sintaxis especial.

y ejecutamos el script mediante:

        python models.py

Con ello, observaremos que se creó el archivo *"libros.db"* el cual contiene nuestra base de datos.

Se puede verificar el contenido de las tablas mediante *sqliteman*[^2]

- - -

La inserción de registros la podemos realizar de la siguiente manera:

~~~
::python

autor_1 = Autor.create(nombre='Patrick Rothfuss')
autor_2 = Autor.create(nombre='Fred Saberhagen')
autor_3 = Autor.create(nombre='Julio verne')

etiqueta_1 = Etiqueta.create(nombre='Ciencia Ficción')
etiqueta_2 = Etiqueta.create(nombre='Fantasía')

libro = Libro.create(titulo='El nombre del viento', isbn='9788401337208')
libro.autores = [a1, a2]
libro.etiquetas = [etiqueta_1]
~~~

Para modificar algún campo solo debemos modificar el atributo y llamar al método *save*:

~~~
::python
autor_3.nombre = 'Julio Verne'
autor_3.save()
~~~

Y las consultas son medainte el método *select* y los filtros mediante el método *where* :

~~~
::python
libro = Libro.select().where(Libro.isbn == '9788401337208')[0]
print(libro.titulo)
~~~

- - -

Espero que el post pueda brindar una idea del cómo funciona **peewee**.


[^1]: Para información más amplia puede guiarse de la [documentación][docs]
[^2]: Sqliteman es un gestor de base de datos para sqlite3

[ORM]: http://es.wikipedia.org/wiki/Mapeo_objeto-relacional
[pip]: https://pypi.python.org/pypi/pip
[peewee-instalacion]: http://docs.peewee-orm.com/en/latest/peewee/installation.html
[docs]: http://docs.peewee-orm.com/en/latest/index.html

[modelo-libros]: /pictures/sqlalchemy-modelo-libros.png 'Modelo de datos'