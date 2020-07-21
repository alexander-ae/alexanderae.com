Title: Búsqueda avanzada con Postgresql y Django - I
Date: 2020-07-20
Tags: django,postgresql
Slug: django-postgres-avanzado-1
Author: __alexander__
Summary: Postgresql es un motor opensource de base de datos, con el cual podemos lograr implementar sistemas de búsqueda complejos sin necesidad de recurrir a motores especializados como elasticsearch. En esta publicación se mostrarán algunas de las características de postgres y el cómo se pueden utilizar mediante Django.

Si tuviéramos que implementar un formulario de búsqueda en django, usualmente recurriríamos al método "filter" de los querysets y a algo como:
 
    .filter(nombre__icontains=q)
    
pero existen situaciones en las que requerimos técnicas más complejas. Y si bien, una opción podría ser utilizar un motor de búsqueda avanzado como *ElasticSearch*, también podríamos usar las características de **postgresql** como:

- trigrams
- unnacent
- full text search (fts)

las cuales iremos revisando a detalle según avanzamos.

<br>
## Entorno de prueba

Para este ejemplo utilizaremos una base de datos que contiene una tabla llamada **Book** (libro).

La tabla "Book" tiene los siguientes campos:

- isbn (identificador único de un libro)
- title
- authors (separados por comas)
- description (reseña)

![estructura de la tabla Book](/pictures/table-books.png)

Para facilitar lo anterior, he preparado un pequeño proyecto en django que se puede descargar de:

* <a target='_blank' href='https://gitlab.com/__alexander__/django-fts-demo'>django-fts-demo</a>

Y un dataset que contiene la lista de 10'000 libros el cual se puede descargar de:
 
* <a target='_blank' href='https://gitlab.com/librera/librera-books-10k'>librera-books-10k</a>

Los pasos a seguir en caso quieran probar con la misma base de datos que utilizo serían:

1. Clonar el proyecto de django
2. Crear una nueva base de datos para el ejemplo y configurarla en el settings de django
3. Ejecutar el siguiente script en el shell de django para importar el CSV a la tabla "Book"

*Nota:* deben remover la primera línea del archivo CSV para que no se importe como un libro (corresponde a la cabecera de la tabla)

~~~
::python
import csv
from books.models import Book

with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        Book.objects.create(
            isbn=row[0],
            title=row[1],
            authors=row[2],
            description=row[3]
        )
~~~

(Opcional) Crear un superusuario de django para poder ingresar al admin.

Con lo anterior podremos observar que ya tenemos los 10k libros:

![10000 libros en el admin](/pictures/django-postgres/admin-10k-books.png)

<br>
## Trigrams

Un **trigram** es un grupo de 3 caracteres tomados de un string.

### Instalando la extensión trigrams en postgresql

Siguiendo la documentación oficial de django:

* <a href="https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/search/#trigram-similarity" target="_blank">trigram similarity</a>
    
Lo que necesitamos en principio es activar la extensión **trigram** de postgres.

*Método 1:* 

La podemos instalar desde el panel de postgres con la sentencia SQL:

~~~
::sql
CREATE EXTENSION pg_trgm;
~~~

Notando que necesitamos ejecutarla con un usuario que tenga permisos para instalar extensiones.

Para lo anterior es posible que se nos requiera instalar el paquete *postgresql-conntrib* respectivo de nuestro sistema operativo.

*Método 2:*

Una alternativa sería crear una migración manual en django similar a:

~~~
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('books', '0001_initial'),
    ]
    operations = [
        TrigramExtension(),
    ]
~~~

Y aplicarla:

    ./manage.py migrate

<br>
### Ejemplo de un trigram

Por ejemplo, para el texto *"Harry Potter"*, postgresql genera los siguientes trigrams:

    {"  h","  p"," ha"," po",arr,"er ",har,ott,pot,rry,"ry ",ter,tte}

lo podemos verificar mediante la consola de postgres con la sentencia:

~~~
::sql
SELECT show_trgm('Harry Potter');
~~~

<br>
### Trigrams en Django - 1er intento

Primero veamos qué sucede si realizamos la búsqueda del texto "Harry Potter" en nuestro formulario:

![resultados de búsqueda iniciales](/pictures/django-postgres/django-filter.png)

Obtenemos 9 resultados con la sentencia:

~~~
::python
Book.objects.filter(title__icontains=q)
~~~

Ahora, siguiente la documentación, utilicemos:

~~~
::python
books = Book.objects.filter(title__trigram_similar=q)
~~~

Observamos lo siguiente:

![resultados de búsqueda con trigrams](/pictures/django-postgres/trigram-01.png)

Tenemos un problema, desaparecieron 2 resultados.

Actualicemos la sentencia para ver qué pasó con los 2 resultados que no fueron contados:

~~~
::python
books = Book.objects.annotate(
            similarity=TrigramSimilarity('title', q),
        ).filter(title__icontains=q).order_by('-similarity')
~~~

Y también actualicemos el html para mostrar el campo "similarity" el cual representa qué tan similar es un resultado comparado a nuestra búsqueda.

Tendremos lo siguiente:

![resultados de búsqueda con trigrams 02](/pictures/django-postgres/trigram-02.png)

Según la documentación de django, solo son tomados los resultados con un valor de "similaridad mayor a 0.3", y según el anterior resultado, dos de nuestros resultados son excluidos.

<br>
### Trigrams en Django - 2do intento

Entonces tal vez nos convenga ajustar este límite a un valor de 0.2 para incluir más resultados:

~~~
::python
books = Book.objects.annotate(
            similarity=TrigramSimilarity('title', q),
        ).filter(similarity__gt=0.2).order_by('-similarity')
~~~

Al realizar nuevamente la búsqueda tendremos:

![resultados de búsqueda con trigrams 03](/pictures/django-postgres/trigram-03.png)

Esta vez obtenemos inclusive un resultado extra ya que comparte cierta similitud con nuestra búsqueda.

<br>
### Ventajas de utilizar trigrams

Al buscar similitudes en vez de coincidencias exactas un usuario puede equivocarse y escribir: *"Harry Porter"* y aún así encontrar algunos resultados:

![resultados de búsqueda con trigrams 04](/pictures/django-postgres/trigram-04.png)

*Nota:*

Como indica la documentación de postgres, para obtener mejores resultados con trigrams, el término a buscar debe tener una longitud similar a los resultados esperados.

Es por ello que al buscar "Harry Porter" las cadenas de resultados más largas muestran una menor similitud.
 
<br>

### A tener en cuenta !

Utilizar trigrams es mucho más pesado (en términos de recursos computacionales) por lo que la búsqueda puede ser más lenta según la cantidad de registros tengamos almacenados en nuestro sistema.

Para mitigar este problema existen los "index", los cuales veremos en una siguiente ocasión.

## Referencias

* <a href="https://www.postgresql.org/docs/current/pgtrgm.html" target="_blank">postgres trigrams</a> 