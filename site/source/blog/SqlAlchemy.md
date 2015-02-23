Title: SqlAlchemy: ORM para python - I
Date: 2013-04-28 16:27
Tags: python, base-de-datos, sqlalchemy,
Slug: sqlalchemy-orm-para-python-1
Author: __alexander__

##### ¿Qué es?

SQLAlchemy es un [ORM][ORM] para python. Incluye soporte para SQLite, MySQL, PostgreSQL, Oracle, MS SQL, entre otros.


##### ¿Qué es un ORM?

Sus siglas significan *Object-Relational mapping*, o en español: *Mapeo Objeto-relacional*. Es una técnica que permite convertir entre los tipos de datos usados en los lenguajes de programación orientados a objetos y los tipos de datos de algun sistema de base de datos relacional.


##### Instalación

Si bien podemos usar [setuptools][setuptools] (easy_install), recomiendo instalarlo mediante [pip][pip].

        pip install sqlalchemy

Para comprobar que se haya realizado la instalación, podemos acceder a la consola interactiva de python y escribir:

~~~
::python

>>> import sql_alchemy
>>> sqlalchemy.__version__
0.8.1
~~~

más información sobre la instalación [aquí][sqlalchemy-instalacion].

- - -

##### Ejemplo de uso

Para ilustrar[^1] la idea, desarrollaré el modelo de datos para un sistema que se encarga de administrar registros de libros, autores, y etiquetas (o temas, para los libros).

El esquema[^2] del modelo es el siguiente:

![modelo-libros][modelo-libros]

Consiste en las tablas Libro, Autor y Etiqueta principalmente.
Las tablas intermediarias *etiqueta_libro* y *autor_libro* se utilizan para expresar la relación de *muchos a muchos* entre las otras tablas.

Primero, debemos mapear el modelo o esquema de la base de datos por medio de sqlalchemy, para lo cual escribí lo siguiente en un archivo al que llamé models.py:


~~~
::python

# -- coding: utf-8 --

from sqlalchemy import (create_engine, Column, Date, Integer, ForeignKey,
    String, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///libros.db', echo=True)
Base = declarative_base()

# relaciones muchos a muchos
etiqueta_libro = Table('etiqueta_libro', Base.metadata,
    Column('libro_id', Integer, ForeignKey('libro.id')),
    Column('etiqueta_id', Integer, ForeignKey('etiqueta.id'))
)

autor_libro = Table('autor_libro', Base.metadata,
    Column('libro_id', Integer, ForeignKey('libro.id')),
    Column('autor_id', Integer, ForeignKey('autor.id'))
)


class Libro(Base):
    __tablename__ = 'libro'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(120), index=True, nullable=False)
    fecha_publicacion = Column(Date)
    isbn = Column(String(13))
    etiquetas = relationship("Etiqueta", secondary=etiqueta_libro)
    autores = relationship("Autor", secondary=autor_libro)

    def __init__(self, titulo, fecha_publicacion, isbn):
        self.titulo = titulo
        self.fecha_publicacion = fecha_publicacion
        self.isbn = isbn

    def __repr__(self):
        return unicode(self.titulo)


class Etiqueta(Base):
    __tablename__ = 'etiqueta'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre


class Autor(Base):
    __tablename__ = 'autor'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

Base.metadata.create_all(engine)

~~~

La explicación va mas o menos así:

1. Importamos los módulos necesarios

2. Realizamos la conexión a la base de datos, en este caso corresponde a sqlite, por medio de un archivo.

3. Mapeamos las tablas como clases, utilizando los tipos de datos de sqlalchemy para expresar los diferentes tipos de datos de sqlite: Integer, String, Date..

4. Añadimos las relaciones entre las tablas: uno a muchos, muchos a muchos..

5. Al final, usamos la sentencia:

        Base.metadata.create_all(engine)

para que al correr el script, se genere la base de datos.

corremos el script mediante:

        python models.py

Con ello, observaremos que se creó el archivo "libros.db" el cual contiene nuestra base de datos.

- - -

El acceso, inserción o modificación de datos, lo podemos realizar de la siguiente manera:

~~~
::python

# -- coding: utf-8 --

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Autor, Etiqueta, Libro

# conexion
engine = create_engine('sqlite:///libros.db', echo=True)
# sesion
Session = sessionmaker(bind=engine)
session = Session()

# insertamos autores
autor_1 = Autor('Patrick Rothfuss')
autor_2 = Autor('Fred Saberhagen')

lista_autores = (autor_1, autor_2)
session.add_all(lista_autores)
session.commit()

# insertamos etiquetas
etiqueta_1 = Etiqueta('aventuras')
session.add(etiqueta_1)

# insertamos libros
libro_1 = Libro('El nombre del fuego', date(2009, 5, 30), '978-8401337208')
libro_1.etiquetas.append(etiqueta_1)
libro_1.autores.append(autor_1)


session.add(libro_1)
session.commit()

# realizando una consulta
libro = session.query(Libro).filter(Libro.isbn=='978-8401337208').first()
print libro

# alterando uno de los atributos
libro.titulo = 'El nombre del viento'
session.commit()

print libro

~~~

El código anterior, se encuentra comentado, indicando los pasos realizados; como la conexión, inserción o modificación de la información.


[^1]: El siguiente ejemplo no busca ser un tutorial completo, sino solamente ejemplificar el funcionamiento básico de sqlalchemy. Para información más amplia puede guiarse de la [documentación][docs] o del siguiente tutorial publicado en [dzone][dzone]
[^2]: El esquema fue realizado con [wwwsqldesigner][wwwsqldesigner]

[ORM]: http://es.wikipedia.org/wiki/Mapeo_objeto-relacional
[setuptools]: https://pypi.python.org/pypi/setuptools
[pip]: https://pypi.python.org/pypi/pip
[sqlalchemy-instalacion]: http://docs.sqlalchemy.org/en/rel_0_8/intro.html#installation
[wwwsqldesigner]: https://code.google.com/p/wwwsqldesigner/
[docs]: http://docs.sqlalchemy.org/en/rel_0_8/
[dzone]: http://python.dzone.com/articles/simple-sqlalchemy-07-08

[modelo-libros]: /pictures/sqlalchemy-modelo-libros.png 'Modelo de datos'