Title: Descargar un archivo y grabarlo en un FileField
Date: 2018-04-19
Tags: django,
Slug: django-descargar-archivo-grabar-model
Author: __alexander__

Estoy desarrollando un proyecto en django y uno de los módulos debe consultar un API externo y descargar imágenes para almacenarlas en un modelo.

Mi dilema fue:

> **¿Cómo descargar un archivo y almacenarlo en un modelo de django?**

### En resumen mi caso fue el siguiente:

*1.* Me conectaba al API de un tercero para obtener cierta información. Yo enviaba un identificador del producto, *un código*.

*2.* El api me retornaba campos como: nombre e *imagen (una url)*

*3.* Para no realizar consultas sucesivas y aprovechar que la información del producto no cambia con el tiempo decidí crear un modelo para almacenar la información recibida en cada consulta.

~~~
::python
   class Producto(models.Model):
       codigo = models.CharField(max_length=20)
       nombre = models.CharField(max_length=20)
       imagen = models.ImageField(upload_to='imagenes', blank=True)
~~~

*4.* En mi aplicación tuve que crear una función que maneje la descarga del archivo y lo registre en el modelo:

~~~
::python
from tempfile import NamedTemporaryFile
from django.core import files
import requests
from .models import Producto


def descarga_producto(codigo, nombre, imagen_url):
    p = Producto(codigo=codigo, nombre=nombre)

    request = requests.get(imagen_url, stream=True)
    if request.status_code != requests.codes.ok:
        return None
    lf = NamedTemporaryFile()
    for block in request.iter_content(1024 * 8):
        if not block:
            break
        lf.write(block)
    producto.imagen.save('filename', files.File(lf))
    producto.save()
~~~

En resumen lo que hace  el código anterior es:

1. Descarga la imagen con la librería requests, notando que activamos el flag "stream" el cual permite descargar el archivo por partes (en caso sea muy grande para no sobrecargar la memoria)

2. Conforme va descargando la imagen, la almacenamos en un **NamedTemporaryFile** que es un archivo temporal que creamos y se almacena en el directorio de archivos temporales que utilicemos ('/tmp' generalmente)

3. Al terminar la descarga, le asignamos un nombre al archivo, lo grabamos y eso es todo.

- - -

**Nota:** no estamos validando que el archivo sea efectivamente una imagen.

#### Referencia

- [Download a remote image and save it to a Django model
](!https://stackoverflow.com/a/16174886/1472750)


