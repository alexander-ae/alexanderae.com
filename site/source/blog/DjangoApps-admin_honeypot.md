Title: Django Apps: admin_honeypot
Date: 2013-01-27 22:50
Tags: django, django-apps, seguridad,
Slug: django-apps-admin_honeypot
Author: __alexander__

En django, por defecto se acostumbra a usar la url **/admin/** como medio de acceso a la interfaz de administración. Sucede que hay quien conociendo esto intenta acceder a dicha url probando algunos usuarios/claves comunes, inclusive por medio de un ataque fuerza bruta con alguna herramienta.

Una medida sencilla con la que podremos filtrar algunos intentos no autorizados de acceso es cambiando esta url por defecto de **/admin/** a alguna otra por ejemplo a **/mi_nuevo_admin/**[^debug].

Pero tal vez aún así queremos saber si alguien intentó acceder a la url por defecto. Allí es donde [django-admin-honeypot][django-admin-honeypot] nos puede ayudar.

Esta aplicación mantiene la url por defecto (/admin) así como la nueva activas. Y en caso de que alguien intente acceder a la url equivocada, nos enviará una notificación por email advirtiendonos del suceso.

#### Instalación

- Requerimos instalar el paquete, lo podemos realizar por medio del clásico pip:

        pip install django-admin-honeypot

- Añadido admin_honeypot a nuestra lista de aplicaciones instaladas:

~~~
::python
INSTALLED_APPS = (
    ...

    'admin_honeypot',

    ...
)
~~~

- Actualizamos nuestras url's (urls.py):

~~~
::python
urlpatterns = patterns(''
    ...
    url(r'^admin/', include('admin_honeypot.urls')),
    url(r'^mi_nuevo_admin/', include(admin.site.urls)),
    ...
)
~~~

#### Notas adicionales

- Podemos ajustar la variable **ADMIN_HONEYPOT_EMAIL_ADMINS** a **True** para permitir que la aplicación envíe un email a los [administradores][admins] del sitio cada vez que se produzca un error de acceso a la falsa url. (Por defecto está en **False**)

- Los intentos de acceso errados son almacenados en la base de datos, siendo los permisos de eliminación de los mismos negados a todos los usuarios[^delete-login]. Esto impide que cualquier usuario 'no autorizado' borre sus huellas.

Si bien solo esta aplicación nos ayuda con parte del problema, es posible que debamos buscar otros complementos/alternativas para mejorar la seguridad del sistema.


[^debug]: Note que esto no nos sería de mucha utilidad si tenemos la variable [debug][debug] como **True** mientras estamos en producción.
[^delete-login]: [Why can’t I delete login attempts from the Django admin?][delete-login]

[admins]: https://docs.djangoproject.com/en/1.5/ref/settings/#admins
[debug]: https://docs.djangoproject.com/en/1.5/ref/settings/#debug
[django-admin-honeypot]: http://django-admin-honeypot.readthedocs.org/en/latest/
[delete-login]: http://django-admin-honeypot.readthedocs.org/en/latest/manual/faq.html#why-can-t-i-delete-login-attempts-from-the-django-admin