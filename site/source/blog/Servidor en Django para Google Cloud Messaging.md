Title: Servidor en django para Google Cloud Messaging para Android (I)
Date: 2014-05-26
Tags: django, android, google-cloud-messaging,
Slug: django-android-google-cloud-messaging-server-1
Author: __alexander__

[Google Cloud Messaging][gcm], para quien aun tenga dudas, es un servicio de google que nos permite enviar[^1] mensajes a los usuarios de nuestra aplicación en *Android*).

Entre otros, podríamos necesitar esta característica para enviar notificaciones, por ejemplo informar sobre la publicación de nuevas ofertas sobre alguno de nuestros productos o incluso para que el dispositivo ejecute ciertas acciones como enviar un mensaje de texto o informar sobre su posición entre muchas otras opciones.

¿Qué debemos hacer para implementar este servicio?

1. Obtener un API key mediante la [consola de desarrolladores de google][gdc].
2. Implementar un servidor, el cual se encargará de enviar la información a nuestra aplicación en android. Nosotros usaremos django.
3. Escribir el cliente en android que será quien reciba la información.

- - -

#### Paso 1: Obteniendo un API Key

1. Abrimos la [consola de desarrolladores][gdc]
2. Creamos un nuevo proyecto.
3. Al crear el proyecto, obtendremos un número único. Dicho número será utilizado luego como el ID del servidor que envia el mensaje (GCM Sender ID).
4. Ingresamos al menú *"API's y autenticación"*, allí se nos listarán las API's de google disponibles. Para nuestro caso, activaremos la que dice "Google Cloud Messaging for Android"
5. Ingresamos al submenú *"Credenciales"* de "API's y autenticación".
6. En el apartado *"Acceso a API Pública"*, clickeamos la opción de "Crear una clave nueva" y escogemos la del tipo "Clave de Servidor".
7. En el nuevo cuadro de diálogo debemos de ingresar la IP de nuestro servidor, para que el API solo acepte conexiones desde allí. Tal y como nos recomienda google, por motivos de prueba podemos ingresar: *0.0.0.0/0*
8. En la nueva página mostrada debemos de copiar la "Clave de la API" que será la que usaremos para autenticar a nuestro servidor de aplicación.

- - -

#### Paso 2: Implementando el servidor en django

*1.* En un nuevo proyecto o uno ya existente, creamos una nueva aplicación que será la que contenga al servidor GCM.

*2.* En el archivo *models.py* de nuestra aplicación creamos un modelo *UsuarioAndroid* que almacenará a cada dispositivo registrado, quedando de la siguiente manera:

~~~
::python
# -*- coding: utf-8 -*-

from django.db import models

class UsuarioAndroid(models.Model):
    android_id = models.CharField('ID Android', max_length=256)

    class Meta:
        verbose_name = 'Usuario Android'
        verbose_name_plural = 'Usuarios Android'

    def __unicode__(self):
        # Al mostrar el usuario, solo mostraremos los 16 primeros caracteres
        # del código asignado.
        return self.android_id[:16]
~~~

*3.* A modo opcional, registramos el modelo en un archivo *admin.py*:

~~~
::python
from django.contrib import admin
from .models import UsuarioAndroid

admin.site.register(UsuarioAndroid)
~~~

*4.* En el archivo *views.py* debemos de crear dos vistas, una de ellas será la que nos muestre el formulario por el cual enviaremos los mensajes y la otra será la que nuestra aplicación en *android* utilizará internamente para registrar un nuevo dispositivo.

También incluyo una función llamada *"gcm_envia_mensaje"* que envía el mensaje por medio del API de GCM.
Se pueden consultar los parámetros en [GCM Server: params][gcm_parametros]

~~~
::python
# -*- coding: utf-8 -*-
from datetime import datetime
import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response as render
from django.template import RequestContext as ctx

import requests

from .models import UsuarioAndroid


def envia_mensaje(request):
    '''
    Vista que muestra un formulario para seleccionar un usuario al que
    enviaremos un mensaje.
    '''
    # listamos los usuarios registrados
    usuarios = UsuarioAndroid.objects.all()

    # en caso de que se suministre un usuario como parametro,
    # enviamos un mensaje.
    usuario = request.GET.get('usuario')

    if usuario:
        gcm_response = gcm_envia_mensaje(usuario)

    return render('envia_mensaje.html', locals(),
        context_instance=ctx(request))


def registra_usuario(request):
    '''
    Registra el android_id de un dispositivo celular.
    '''
    android_id = request.GET.get('usuario_id')
    usuario, status = UsuarioAndroid.objects.get_or_create(
        android_id=android_id)

    return HttpResponse(str(status))


# UTIL

def gcm_envia_mensaje(android_id, mensaje='Hola'):
    '''
    Función que recibe el código de un dispositivo como parámetro y le envia un
    mensaje.
    '''
    try:
        usuario = UsuarioAndroid.objects.get(android_id=android_id)
    except UsuarioAndroid.DoesNotExist:
        return HttpResponse('El usuario no existe')

    URL = 'https://android.googleapis.com/gcm/send'

    # Parámetros a enviar
    data = {
        'registration_ids': [str(usuario.android_id)],
        'restricted_package_name': settings.GCM_PACKAGE,
        'collapse_key': str(datetime.now()),
        'data': {
            'server': 'my-server-name',
            'msg': mensaje
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + settings.GCM_API_SERVER_KEY
    }

    # iniciamos el request
    r = requests.post(URL, data=json.dumps(data), headers=headers)

    STATUS_CODES = {
        200: 'Ok',
        400: 'JSON error',
        401: 'Ha fallado la autenticacion',
        500: 'Error',
        501: 'Servidor no disponible'
    }

    status = STATUS_CODES[r.status_code]

    response = {
        'estado': 'error',
        'detalle_de_estado': status,
        'texto': r.text
    }

    if r.status_code == 200:
        response['estado'] = 'ok'

    return response

~~~

*5.* Añadimos el template html de nuestro formulario, en el archivo *envia_mensaje.html*:

~~~
::html
<html>
    <head></head>

    <body>
        <form action="#">
            {% if usuarios %}
                <select name="usuario">
                    {% for u in usuarios %}
                        <option value="{{ u.android_id }}">{{ u }}</option>
                    {% endfor %}
                </select>

                <input type="submit" value='Enviar mensaje'>
            {% else %}
                <span>No hay usuarios registrados</span>
            {% endif %}
        </form>

        {% if gcm_response %}
            <div id="resultado">
                <p>Estado: {{ gcm_response.estado }}</p>
                <p>Detalle del código de estado: {{ gcm_response.detalle_de_estado }}</p>
                <p>Respuesta: {{ gcm_response.texto }}</p>
            </div>
        {% endif %}
    </body>
</html>
~~~

*6.* Por último, en nuestro archivo *settings.py*, no olvidemos registrar nuestra aplicación en la variable *INSTALLED_APPS*, asi como añadir las variables de configuración[^2] de nuestro servidor y el nombre de nuestro paquete en Android:

~~~
::python
# GCM
GCM_PACKAGE = 'com.alexanderae.demo_gcm'
GCM_API_SERVER_KEY = 'AIzaSyCLK22vGoi6Gz663oIE9kTXZeTYC5lS4ww'
~~~

- - -

El próximo paso será el implementar nuestra aplicación en android.

Para leer a detalle sobre la implementación de un servidor GCM con django, se puede consultar la [documentación][gcm_server_docs].

Pueden consultar el código del proyecto de prueba que realicé en un repositorio en [bitbucket][repo-server].

<br/>

*Nota:* Este proyecto tiene como finalidad el mostrar cómo escribir un servidor para GCM desde cero, pero para fines más serios, es posible que se desee utilizar algún proyecto como: [django-gcm][django_gcm].

<br/>

[^1]: También es posible recibir información desde el dispositivo mediante la misma conexión, pero para este ejemplo solo enviaré la información en un sentido.
[^2]: Note que en un entorno de producción, las variables de configuración *no deben de mostrarse en el archivo settings*, sino que debemos utilizar variables de entorno o algún otro método.

[gcm]: http://developer.android.com/google/gcm/index.html
[gdc]: https://cloud.google.com/console
[gcm_parametros]: http://developer.android.com/google/gcm/server.html#params
[gcm_server_docs]: http://developer.android.com/google/gcm/server.html
[repo-server]: https://bitbucket.org/__alexander__/demo-django-gcm-server
[django_gcm]: https://github.com/bogdal/django-gcm