Title: Convertir un archivo CSV a SQLite con Python
Date: 2020-03-24
Tags: python,
Slug: convertir-csv-sqlite-python
Author: __alexander__
Summary: Instrucciones para convertir un archivo CSV a un archivo SQLite. SQLite viene con su propia línea de comandos para realizar algunas tareas, entre ellas, la importación de archivos CSV.

#### ¿Qué es un archivo CSV?

Un archivo **CSV** (Comma Separated Values) es un archivo que contiene datos separados por comas (u otros separadores como tabuladores, espacios, puntos y coma, etc). En estos archivos cada línea representa un registro.

Por ejemplo, este archivo toma la forma:

~~~
Código, Nombre, Departamento
014285, Colegio Belén, Lima
028514, IIEE 2042, Arequipa
042857, Colegio Toribianitos, Lima
~~~

#### ¿Cómo convertir un archivo CSV a un archivo SQLITE?

SQLite viene con su propia línea de comandos para realizar algunas tareas, entre ellas, la importación de archivos CSV.

~~~
::sqlite
>>> sqlite3
>>> sqlite> .mode csv
>>> sqlite> .import input.csv table_name
>>> sqlite> .schema table_name
>>> sqlite> .save output.db
~~~

Lo que acabamos de realizar es:

1. Activar el modo CSV (.mode csv)
2. Importar el archivo en la tabla indicada
3. Verificamos el script utilizado para crear la tabla anterior
4. Exportamos el archivo a una base de datos *sqlite*
5. Fin :)

#### ¿Por qué no uso python?

En mi caso, el archivo utilizado tenía 170k+ registros y no requería la modificación de sus registros previo a la inserción, por lo que utilizar python era mucho más lento y terminé usando la shell de sqlite directamente.

#### ¿Cómo convertir un archivo CSV a SQLite con Python?

Dependiento de nuestras necesidades podemos:

1. Utilizar un ORM para generar el código SQL (Pewee ORM, PonyORM, etc)
2. Utilizar pandas
3. Utilizar dataset (o en general alguna otra librería), por ejemplo:

~~~
::python
import csv, uuid, dataset


def csv2dataset(filename_input, filename_output):
    with open(filename_input, 'r') as file_input:
        input_data = csv.DictReader(file_input)
        db = dataset.connect('sqlite:///' + filename_output)
        table = db['contactos']
        for contact in input_data:
            contact['uuid'] = uuid.uuid4().hex
            table.insert(contact)


if __name__ == '__main__':
    csv2dataset('direcciones.csv', 'direcciones.sqlite')
~~~

#### Referencias

1. <a target='_blank' href='https://sqlite.org/cli.html'>Command Line Shell for SQLITE</a>
2. <a target='_blank' href='https://www.sqlitetutorial.net/sqlite-import-csv/'>Import a CSV File Into an SQLite Table</a>
3. <a target='_blank' href='https://www.sqlitetutorial.net/sqlite-import-csv/'>Dataset</a>
4. <a target='_blank' href='https://blog.lordvan.com/blog/python-dataset-library-csv-to-sqlite/'>Python Dataset Library -- CSV to SQLite</a>
