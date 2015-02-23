Title: Awesome Django
Date: 2015-01-24
Tags: django,django-apps,python,
Slug: awesome-django-apps
Author: __alexander__


Si tuviera que enumerar los motivos por los que utilizo [django][django], serían: [python][python], su [filosofía][django-filosofia] y su [comunidad][django-comunidad].

En este post plasmo una pequeña recopilación de aplicaciones y proyectos de terceros que me han facilitado el programar con django, esperando que a alguién más le sea de utilidad.

Aunque tal vez me olvide de uno que otro, aquí va mi lista:

- - -

#### 1. Django debug toolbar

[https://github.com/django-debug-toolbar/django-debug-toolbar][django-debug-toolbar]

Conjunto de paneles configurables que muestran información que ayuda al proceso de hacer debug del request actual. Algunos de ellos son:

- Versiones: para conocer la versión de python, django y otros paquetes utilizados
- SQL: muestra la lista de consultas SQL invocadas en el request.
- Configuraciones: lista de variables del archivo settings
- Templates: plantillas html renderizadas
- otros..


#### 2. Django grappelli

[https://github.com/sehmaschine/django-grappelli][django-grappelli]

Es un "tema" para reemplazar a la apariencia por defecto del admin de django.
Cuenta además con varias utilidades para hacer el uso del admin más personalizable.


#### 3. Django Filebrowser

[https://github.com/sehmaschine/django-filebrowser][django-filebrowser]

Gestor de archivos media para el admin de django.
Nota: es del mismo desarrollador de *grappelli* por lo que se integran perfectamente.


#### 4. Django Admin Honeypot

[https://github.com/dmpayton/django-admin-honeypot][django-admin-honeypot]

Un falso login para el admin de django que notifica a los administradores de intentos de acceso desautorizados.


#### 5. Django Ratelimit

[https://github.com/jsocol/django-ratelimit][django-ratelimit]

Decorador que restringe el acceso a determinadas vistas (views) en base a ciertos parámetros como por ejemplo, el número de consultas realizadas por una IP en cierto intervalo.


#### 6. Django Nose

[https://github.com/django-nose/django-nose][django-nose]

Todas las bondades de [nose][nose] para django.


#### 7. Django Extensions

[https://github.com/django-extensions/django-extensions][django-extensions]

Conjunto de comandos adicionales para la administración del proyecto (manage.py).
Entre las utilidades destacan:

- shell_plus: shell que auto carga los modelos de nuestra aplicación.
- runscript: ejecuta un script en el contexto de nuestro proyecto.
- show_urls: muestra la lista de todas las url's.
- graph_models: permite visualizar nuestros modelos en un diagrama.


#### 8. Django Celery

[http://celery.readthedocs.org/en/latest/index.html][celery]

Gestor de colas distribuido.


#### 9. Django RQ

[https://github.com/ui/django-rq][django-rq]

Provee integración entre [RQ][rq] y django. *RQ* es un gestor de colas que utiliza **redis** como backend. Su objetivo es ser una alternativa ligera a *celery*.


#### 10. Django Sentry

[https://github.com/getsentry/sentry][sentry]

Sentry es un proyecto que nos ayuda en las tareas de detección, registro y agrupación de los errores de nuestro proyecto.


#### 11. Python Social Auth

[https://github.com/omab/python-social-auth][python-social-auth]

Aplicación para gestionar la autenticación y registro en diversas plataformas sociales (facebook, twitter, etc).


#### 12. Django Taggit

[https://github.com/alex/django-taggit][django-taggit]

Sistema de gestión de etiquetas en nuestros modelos.


#### 13. Django Geoposition

[https://github.com/philippbosch/django-geoposition][django-geoposition]

*Model field*[^1] que permite insertar coordenadas geolocalizadas con ayuda de google maps.


#### 14. Django Recaptcha

[https://github.com/praekelt/django-recaptcha][django-recaptcha]

*Form field*[^1] para insertar un recaptcha en los formularios.


#### 15. Django Mptt

[https://github.com/django-mptt/django-mptt][django-mptt]

Utilidades para implementar un modelo que almacena información jerárquica.
Por ejemplo, un sistema de categorías anidadas.


#### 16. Django Redis

[https://github.com/niwibe/django-redis][django-redis]

Aplicación que permite utilizar redis como un backend de cache.


#### 17. Django Summernote

[https://github.com/summernote/django-summernote][django-summernote]

Editor [wysiwyg][^2] para django.


#### 18. Sorl Thumbnail

[https://github.com/mariocesar/sorl-thumbnail][sorl-thumbnail]

Gestor de miniaturas.


#### 19. Django ModelTranslation

[https://github.com/deschler/django-modeltranslation][model-translation]

Traduce nuestros modelos utilizando un enfoque similar al del admin (por medio de registros).


#### 20. Restless

[https://github.com/toastdriven/restless][restless]

Miniframework REST ligero.


#### 21. Django Watchman

[https://github.com/mwarkentin/django-watchman][django-watchman]

Genera una url para mostrar el estado de algunos backends (cache, database, email).


#### 22. Django Simple Captcha

[https://github.com/mbi/django-simple-captcha][django-simple-captcha]

Generador de captchas simples.


#### 23. Django uuslug

[https://github.com/un33k/django-uuslug][django-uuslug]

Generador de slug's unicode únicos.


#### 24. Supervisor

[https://github.com/Supervisor/supervisor][supervisor]

Sistema de control de procesos para UNIX. Lo he utilizado para monitorizar y reiniciar automáticamente algunos demonios (uwsgi, colas).


#### 25. Fabric

[http://www.fabfile.org/][fabric]

Herramienta de línea de comandos que facilita tanto el despliegue de aplicaciones como las tareas de administración de un sistema.


#### 26. uwsgi

[https://uwsgi-docs.readthedocs.org/en/latest/][uwsgi]

Servidor de aplicaciones para python (soporta otros lenguajes).
Lo utilizo generalmente en conjunto con nginx como servidor web.

#### 27.  Pillow

[https://github.com/python-pillow/Pillow][pillow]

Fork de *PIL*, es una librería de manipulación de imágenes de python.


#### 28. Unidecode

[https://github.com/iki/unidecode][unidecode]

Transliteración de texto unicode. Permite representar texto unicode en ASCII.

#### 29. PEP 8

[https://github.com/jcrocholl/pep8][pep8]

Herramienta de checkeo de estilos.

- - -

Referencias:

- [33 projects that make developing django apps awesome][33-awesome-django]
- [Why django is awesome][why-django-is-awesome]
- [Django Packages][django-packages]
- [Awesome Django][awesome-django]


[django]: https://www.djangoproject.com/
[python]: https://www.python.org/
[django-filosofia]: https://docs.djangoproject.com/en/dev/misc/design-philosophies/
[django-comunidad]: https://www.djangoproject.com/community/

[django-debug-toolbar]: https://github.com/django-debug-toolbar/django-debug-toolbar
[django-grappelli]: https://github.com/sehmaschine/django-grappelli
[django-filebrowser]: https://github.com/sehmaschine/django-filebrowser
[django-admin-honeypot]: https://github.com/dmpayton/django-admin-honeypot
[django-ratelimit]: https://github.com/jsocol/django-ratelimit

[django-nose]: https://github.com/django-nose/django-nose
[nose]: http://nose.readthedocs.org/en/latest/
[django-extensions]: https://github.com/django-extensions/django-extensions
[celery]: http://celery.readthedocs.org/en/latest/index.html
[django-rq]: https://github.com/ui/django-rq

[rq]: https://github.com/nvie/rq
[sentry]: https://github.com/getsentry/sentry
[python-social-auth]: https://github.com/omab/python-social-auth
[django-taggit]: https://github.com/alex/django-taggit
[django-geoposition]: https://github.com/philippbosch/django-geoposition

[django-recaptcha]: https://github.com/praekelt/django-recaptcha
[django-mptt]: https://github.com/django-mptt/django-mptt
[django-redis]: https://github.com/niwibe/django-redis
[django-summernote]: https://github.com/summernote/django-summernote
[sorl-thumbnail]: https://github.com/mariocesar/sorl-thumbnail

[model-translation]: https://github.com/deschler/django-modeltranslation
[restless]: https://github.com/toastdriven/restless
[django-watchman]: https://github.com/mwarkentin/django-watchman
[django-simple-captcha]: https://github.com/mbi/django-simple-captcha
[supervisor]: https://github.com/Supervisor/supervisor

[fabric]: http://www.fabfile.org/
[uwsgi]: https://uwsgi-docs.readthedocs.org/en/latest/
[pillow]: https://github.com/python-pillow/Pillow
[unidecode]: https://github.com/iki/unidecode
[pep8]: https://github.com/jcrocholl/pep8

[33-awesome-django]: http://elweb.co/33-projects-that-make-developing-django-apps-awesome/
[why-django-is-awesome]: http://www.leucinerichbio.com/why-is-django-awesome/
[django-packages]: https://www.djangopackages.com/
[awesome-django]: https://github.com/rosarior/awesome-django
[django-uuslug]: https://github.com/un33k/django-uuslug

[^1]: No se me ocurre ninguna traducción adecuada.
[^2]: Lo que ves es lo que obtienes (o al menos esa es la idea)