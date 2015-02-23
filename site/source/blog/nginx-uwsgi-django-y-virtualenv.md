Title: nginx, uwsgi, django y virtualenv
Date: 2013-09-28 10:14
Tags: nginx, django, webfaction, uwsgi,
Slug: nginx-uwsgi-django-y-virtualenv
Author: __alexander__

Este es un breve tutorial que indica como configurar django en un servidor de producción por medio de [nginx][nginx], [uwsgi][uwsgi] y [virtualenv][virtualenv].

En mi caso, seguí estas indicaciones en [webfaction][webfaction] sin ningún problema.

#### nginx: instalación

~~~
::sh
mkdir -p ~/{opt,projects,src}
cd ~/src
wget http://nginx.org/download/nginx-1.5.x.tar.gz
tar xf nginx-1.5.x.tar.gz
cd nginx-1.5.x
./configure --prefix=/home/username/opt/nginx  --with-http_ssl_module
make && make install
~~~


#### uwsgi

instalamos uwsgi

        pip install uwsgi

creamos un archivo de prueba:

~~~
::python
# test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hola mundo cruel"
~~~

lanzamos uwsgi[^2] indicando el archivo que creamos:

        uwsgi --http :16517 --wsgi-file test.py

y si todo va bien.. podemos continuar


#### django y virtualenv[^1]

creamos un entorno virtual, instalamos django y creamos un proyecto de prueba.

        mkvirtualenv django
        pip install django
        cd ~/projects
        # creamos un proyecto de prueba
        django-admin startproject myapp

para que el entorno virtual sea reconocido adecuadamente, editamos el archivo wsgi.py de nuestro proyecto en django para que quede de la siguiente manera:

~~~
::python
# wsgi.py
import os
import sys

from site import addsitedir
addsitedir('/home/username/.envs/django_1_5/lib/python2.7/site-packages')

sys.path = ['/home/username/projects/myapp/',
'/home/username/projects/myapp/myapp/'] + sys.path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = get_wsgi_application()
~~~

y podemos probar uwsgi con nuestro proyecto en django:

        uwsgi --http :16517  --wsgi-file /home/username/projects/myapp/myapp/wsgi.py

---

Si todo bien hasta ahora, podemos configurar nginx para que interactue con uwsgi.

        nginx <-> uwsgi <-> django



---

#### nginx: configuración
editamos el archivo nginx.conf para que quede similar a:

~~~
# nginx.conf
worker_processes  1;

error_log  logs/error.log;

events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  logs/access.log  main;

    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       16517;
        server_name  nginx1.username.webfactional.com;

        location / {
            include uwsgi_params;
            uwsgi_pass unix:///home/username/projects/myapp/myapp.sock;
        }
    }
}
~~~

ejecutamos el worker de uwsgi:

        uwsgi --master --workers 1 --wsgi-file /home/username/projects/myapp/myapp/wsgi.py --uwsgi-socket /home/username/projects/myapp/myapp.sock

iniciamos nginx:

        ~/opt/nginx/sbin/nginx

Y con esto concluye lo básico. Si me doy un tiempo, ampliaré esta entrada con lo necesario para que nginx maneje los archivos static y media de nuestro proyecto en django así como también el añadir a un gestor de procesos como supervisor para que maneje los workers de uwsgi.

##### Información adicional:

1. [Setting up Django and your web server with uWSGI and nginx][nginx-uwsgi-django]
2. [How to use Django with uWSGI][django-uwsgi]
3. [Deploy Django-Nginx-uwsgi pada web faction][webfaction-nginx-uwsgi-django]


[^1]: Note que estoy usando [virtualenvwrapper][virtualenvwrapper] para administrar el entorno virtual (mkvirtualenv para crear el entorno virtual).

[^2]: si estamos usando *webfaction* debimos de haber creado, por medio de su [panel][webfaction-apps], una aplicación personalizada y utilizado el puerto que se nos asigno para la prueba con uwsgi o con nginx (en mi caso el 16517)


[nginx]: http://nginx.org/
[uwsgi]: http://projects.unbit.it/uwsgi/
[virtualenv]: https://pypi.python.org/pypi/virtualenv
[webfaction]: https://www.webfaction.com/
[virtualenvwrapper]: http://virtualenvwrapper.readthedocs.org/en/latest/
[webfaction-apps]: https://my.webfaction.com/applications
[nginx-uwsgi-django]: https://uwsgi.readthedocs.org/en/latest/tutorials/Django_and_nginx.html
[django-uwsgi]: https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/uwsgi/
[webfaction-nginx-uwsgi-django]:https://gist.github.com/widoyo/4406049