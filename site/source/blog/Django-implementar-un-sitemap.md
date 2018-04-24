Title: Implementar un sitemap en django
Date: 2018-04-24
Tags: django,seo,
Slug: django-implementar-sitemap
Author: __alexander__

Continuando con un proyecto personal, esta vez tuve que implementar un archivo **sitemap.xml**.

### ¿Qué es el archivo sitemap.xml?

Es un archivo que los indexadores o "search engines" como google o bing utilizan para descubrir las páginas en nuestros websites. Ya que si bien los buscadores pueden "escanear" nuestra página sin ayuda hay casos en los que se recomienda incluir un sitemap (ver sección de *"Información adicional"*).

### ¿Cómo implementar un sitemap en django?

Django cuenta con una aplicación oficial para la creación de sitemaps. Siguiendo su documentación, los  pasos a seguir son:

**1.** Agregar 'django.contrib.sitemaps' a INSTALLED_APPS


**2.** Asumiendo que tenemos una aplicación llamada "libros", podríamos crear el archivo *"libros/sitemaps.py"*

*libros/models.py*:

django genera la url con el método *get_absolute_url*

~~~
::python
class Libro(models.Model):
    nombre = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, blank=True)
    
    def get_absolute_url(self):
        return reverse('libros:libro', kwargs={'slug': self.slug})
~~~

*libros/sitemaps.py*
~~~
::python
from django.contrib.sitemaps import Sitemap
from .models import Libro


class LibroSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    protocol = 'http'

    def items(self):
        return Libro.objects.all()
~~~

**3** Registramos el sitemap en el archivo *urls.py*:

~~~
::python
from django.contrib.sitemaps.views import sitemap
from libros.sitemaps import LibroSitemap

sitemaps = {
    'libros': LibroSitemap,
}

urlpatterns = [
    ..
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]
~~~

**4** Visitamos la dirección **/sitemap.xml** y eso sería todo.

- - -

### Preguntas frecuentes
<br>
**- ¿puedo tener un sitemap por cada aplicación?**

Si quisiéramos agregar otro sitemap, por ejemplo para nuestras páginas estáticas podríamos realizar algo como:

*pages/sitemaps.py*

~~~
::python
from django.contrib import sitemaps
from django.urls import reverse


class PageSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['home', 'sobre-nosotros', 'contacto']

    def location(self, item):
        return reverse(item)

~~~

*urls.py* : solo incluyo las secciones nuevas o que han cambiado
~~~
::python
..
from pages.sitemaps import PageSitemap

sitemaps = {
    'pages': PageSitemap,
    'libros': LibroSitemap,
}
~~~
 
**- ¿Qué pasa si mi sitemap tiene más de 50 000 páginas?**

Django permite crear un *index* para nuestro sitemaps, se recomienda revisar la [documentación](!https://docs.djangoproject.com/en/2.0/ref/contrib/sitemaps/#creating-a-sitemap-index)

**- Mi sitemap tiene muchas páginas, es muy lento de procesar ¿y ahora quién podrá defenderme?**

se puede utilizar el decorador *cache_page* de django, ya que no tiene sentido realizar un cálculo muy frecuente, cuando nuestros contenidos se actualizan diariamente o semanalmente.

**- ¿cómo puedo utilizar https en mis sitemap?**

utiliza el parámetro *protocol*.

<br>
### Información adicional

1. [¿Necesito un sitemap?](!https://support.google.com/webmasters/answer/156184?hl=es)

2. [Documentación de django sobre la creación de un sitemap](!https://docs.djangoproject.com/en/2.0/ref/contrib/sitemaps/)