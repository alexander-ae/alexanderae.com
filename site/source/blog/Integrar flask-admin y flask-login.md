Title: Integrar flask-admin y flask-login
Date: 2013-05-19 15:00
Tags: python, flask,
Slug: integrar-flask-admin-y-flask-login
Author: __alexander__

Para quien aun no esté enterado, [**Flask**][flask] es un microframework web para **python**.

Flask cuenta con varias [extensiones][extensions], de entre las cuales [flask-admin][flask-admin] nos provee de una interfaz administrativa y [flask-login][flask-login] se encarga de manejar un sistema de autenticación para nuestras vistas.

El problema aparece cuando necesitamos que la interfaz de administración incluya un sistema de autenticación (nos referimos a un login). En la [documentación][flask-admin-docs] de flask-admin nos indican:

> By default, administrative interface is visible to everyone, as Flask-Admin does not make any assumptions about authentication system you’re using.


> If you want to control who can access administrative views and who can not, derive from the administrative view class and implement is_accessible method.


O dicho de otro modo, flask-admin no incluye ningún sistema de autenticación ni tampoco está restringido a algún paquete en especial para encargarse de esta tarea.

Lo que sí nos indican es que es posible implementar un método is_accessible como sigue:

~~~
::python
class MyView(BaseView):
    def is_accessible(self):
        return login.current_user.is_authenticated()
~~~

Con ello lograremos que solo los usuarios autenticados puedan acceder a dicha vista admininistrativa, pero aquellos usuarios que no se han logueado obtendrán un error 404.

Lo ideal sería que al no estar logueados, se nos redirigiese hacia la página del login, pero el método anterior se limita a mostrarnos una pantalla de error.

Otra manera de integrar el login y el admin sería utilizando una vista personalizada. Por defecto la vista principal del admin se ve como:

~~~
::python
class AdminIndexView(admin.AdminIndexView):
    @admin.base.expose()
    def index(self):
        return self.render(self._template)
~~~

Entonces, podríamos editar la vista por defecto para que al no detectar al usuario como logueado, se nos redirija al login:

~~~
::python
# admin.py
from flask import redirect, url_for
from flask.ext import admin, login

from views import app


class MyAdminIndexView(admin.AdminIndexView):
    @admin.base.expose()
    def index(self):
        is_auth = login.current_user.is_authenticated()
        if is_auth:
            return self.render(self._template)
        else:
            return redirect(url_for('login'))

admin_ = admin.Admin(app, 'Auth', index_view=MyAdminIndexView())
~~~

Y con ello obtendríamos lo esperado.

Notar que nos faltaría encargarnos del acceso a las vistas internas y también del añadir un link para finalizar nuestra sesión.



[flask]: http://flask.pocoo.org/
[extensions]: http://flask.pocoo.org/extensions/
[flask-admin]: https://github.com/mrjoes/flask-admin
[flask-login]: https://github.com/maxcountryman/flask-login
[flask-admin-docs]: https://flask-admin.readthedocs.org/en/latest/quickstart/#authentication