Title: Django, MySQL y Apache en Windows Server
Date: 2013-04-11
Tags: django, windows-server
Slug: django-mysql-apache-en-windows-server
Author: __alexander__

Hasta hace poco, no había tenido la necesidad de configurar django en un entorno en producción en windows, por suerte para mi, fue un tanto menos complicado de lo esperado. Lo que a mi me tocó usar fue Python 2.7, Django 1.4, WAMP (Apache + MySQL), todo ello en Windows Server. A continuación, un resumen de lo que hice:

*1.* Instalamos la versión de *python* requerida (por ejemplo la 2.7.4), la cual podemos obtener de [python.org][python.org].

*2.* Instalamos *setuptools*, una herramienta de gestión de paquetes para python. Lo podemos descargar desde [pypi][setuptools].
No olvidar que debemos de escoger la versión adecuada para nuestra versión de python instalada.

*3.* Añadir al path el directorio de python y sus scripts, por ejemplo:

    C:\Python27;C:\Python27\Scripts;..

Podemos comprobar lo realizado hasta aquí, ingresando a la ventana de comandos (cmd):

Al escribir python y presionar enter, se debe de mostrar la consola interactiva de python. Para salir, presione *ctrl + z + enter*.

Al escribir easy_install se nos debe de comunicar que nos faltó indicar la url o ruta del archivo a instalar.

*4.* Instalamos [pip][pip] (otro gestor de paquetes de python) mediante:
    
    easy_install pip

*5.* Instalamos django y las dependencias de nuestro proyecto por medio de pip, por ejemplo:

    pip install "django<=1.4.99"
    pip install "django-uuslug"

*6.* En caso de requerir [PIL][PIL] (Python Imaging Library) en nuestro proyecto, se recomienda utilizar [Pillow][pillow] (un fork de PIL mucho más amigable que su antecesor) como reemplazo. Puede descargar el instalador para windows desde [pypi][pypi-pillow] 

- - - 


*7.* Descargamos e instalamos [WAMP Server][wamp]. Note que se requiere como dependencia a [Microsoft Visual C++ 2010 Redistributable][visual-2010] (observe que puede descargar la versión x86 o la de 64 bits). Una vez instalado wamp, podemos cargar nuestra base de datos por medio de *phpMyAdmin*

*8.* Descargamos e instalamos el conector de python para mysql, lo podemos descargar desde [sourceforge][mysql-python].
Note que debemos escoger la versión que corresponda a nuestro python instalado.

- - -

*9.* Descargamos nuestro proyecto en django mediante [filezilla][filezilla] o cualquier otra herramienta.

*10.* Configuramos la base de datos en el archivo [settings.py][settings.py]. Para comprobar si el proyecto inicia en modo "desarrollo", podemos abrir el cmd y escribir:

    python manage.py runserver

Ir a la ruta [http://127.0.0.1:8000][local-8000] y observar si el sitio web se visualiza de forma correcta.

*11.* Configuramos la ruta para el directorio static con el parámetro:

    STATIC_ROOT

recolectamos los archivos static:

    python manage.py collectstatic

*12.* Configuramos el archivo wsgi para que quede similar a:

    import os, sys  
      
    sys.path = ['C:\proyecto\www', 'C:\Python27\Lib\site-packages'] + sys.path
      
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
      
    import django.core.handlers.wsgi

    application = django.core.handlers.wsgi.WSGIHandler()



*13.* Descargamos el módulo [mod_wsgi][mod_wsgi] para apache, el cual permite conectar el mismo con nuestras aplicaciones en python que soporten [wsgi][wsgi].
Una vez descargada la versión correspondiente a nuestro python, renombramos el archivo a **mod_wsgi.so** y lo copiamos a la carpeta *modules* de nuestro apache, la cual puede tener una ruta similar a:

    C:\wamp\bin\apache\apache2.2.22\modules

*14.* Configuramos apache, por medio del archivo *httpd.conf*

Añadimos el módulo mod_wsgi
>    LoadModule wsgi_module modules/mod_wsgi.so

Añadimos el archivo wsgi y la configuración para los directorio static y media:

    Alias /media/ "C:\proyecto\www\media\"
    Alias /static/ "C:\proyecto_static\"

    <Directory C:\proyecto\www\media\>
        Order deny,allow
        Allow from all
    </Directory>

    <Directory C:\proyecto_static\ >
        Order allow,deny
        Allow from all
    </Directory>


    WSGIScriptAlias / "C:\proyecto\www\wsgi.py"

    WSGIPythonPath "C:\proyecto\www"

    <Directory "C:\proyecto\www">
        <Files wsgi.py>
        Order deny,allow
        Allow from all
        </Files>
    </Directory>

Reiniciamos apache, y al acceder al localhost deberíamos poder visualizar nuestro proyecto.


[python.org]: http://python.org/download/
[setuptools]: https://pypi.python.org/pypi/setuptools#downloads
[pip]: https://pypi.python.org/pypi/pip
[PIL]: http://www.pythonware.com/products/pil/
[pillow]: http://python-imaging.github.io/Pillow/
[pypi-pillow]: https://pypi.python.org/pypi/Pillow/2.0.0
[wamp]: http://www.wampserver.com/en/
[visual-2010]: http://www.microsoft.com/download/en/details.aspx?id=13523
[mysql-python]: http://sourceforge.net/projects/mysql-python/
[filezilla]: https://filezilla-project.org/
[settings.py]: https://docs.djangoproject.com/en/dev/topics/settings/
[local-8000]: http://127.0.0.1:8000
[mod_wsgi]: https://code.google.com/p/modwsgi/
[wsgi]: http://wsgi.readthedocs.org/en/latest/what.html
