Title: Django Apps: uuslug
Date: 2013-06-23 23:00
Tags: django, django-apps,
Slug: django-apps-uuslug
Author: __alexander__

Una de las características de **[django][django]** es el [diseño elegante][design-your-urls] de las urls a diferencia de como otros frameworks o lenguajes puedan manejar este aspecto. Por ejemplo con asp o php podríamos tener[^1]:

    www.test.com/post.asp?u=142

    www.test.com/post.php?u=142

Mientras que en *django* podríamos tener sin problema, urls amigables como:

    www.test.com/post/142

- - -

Nota: debemos considerar que utilizar id's en nuestras urls no es recomendable:

1. Hay quien opina que facilita ataques por inyección sql. Aunque en django tenemos ese punto cubierto al utilizar correctamente los [querysets][django-sql-injection].

2. También hay quienes creen que afecta al [SEO][seo]. En un [artículo de google][dynamic-urls-vs-static-urls], nos explican a más detalle el problema en cuestión.

3. A mi parecer el motivo más importante es por el tema de la [usabilidad][usabilidad]. Para el usuario las urls sencillas son más fáciles de copiar, recordar y también el encontrar lo que se busca. Tal y como vi en una respuesta de [stackoverflow][stackoverflow], entre estas dos urls:

> www.test.com/page.php?u=85583

> www.test.com/solution-to-your-problem.php

un usuario tendería a escoger la segunda url por motivos que resultan obvios.

- - -

Entonces después de esta no tan breve introducción.. ¿cómo realizamos esto con django?

**Django**, en su módulo *utils* dispone de la función [slugify][django-slugify] para generar slugs[^2] y en su módulo *models* tenemos a [SlugField][django-slugfield] para autogenerar un campo de este tipo.

El problema aparece cuando por ejemplo generamos los campos *slug* en base a el título de una noticia, la cual para el ejemplo se titula: *Explosión* y pasado cierto tiempo aparece otra noticia llamada del mismo modo.

La función que genera slug's por defecto en django tiene los dos siguientes problemas:

- No genera slugs para términos con caracteres no ascii, como lo son las tildes.
- No toma en cuenta que el término base pueda aparecer varias veces y al generar el mismo slug puede crearse un conflicto al acceder a la url.

El paquete que utilizo para solventar este inconveniente es [django-uuslug][django-uuslug]

#### Instalación

Tan sencillo como siempre:

    pip install django-uulug

#### ¿Cómo usar?

Para generar un slug cualquiera, podemos usar su propia función *slugify*:

~~~~
::python
>>> from uuslug import slugify
>>> slugify('This is a test ---')
    'this-is-a-test'
>>> slugify('explosión')
    'explosion'
~~~~

Y si deseamos autogener un slug único en un modelo, por ejemplo para el caso de las noticias:

~~~~
::python

from django.db import models
from uuslug import uuslug

class Noticia(models.Model):
    titulo = models.CharField(max_length=100)
    slug = models.CharField(max_length=200)

    def __unicode__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.titulo, instance=self)
        super(Noticia, self).save(*args, **kwargs)
~~~~

y con ello, para noticias con el mismo título se añade un número al final del slug para que queden como: noticia, noticia-1, etc.

#### urls

En nuestras urls tendremos algo como:

~~~~
::python
url(r'^noticia/(?P<slug>[-\w]+)$', 'views.noticia')
~~~~

para finalmente el poder utilizar las url's:

> noticia/explosion

> noticia/explosion-1

[^1]: Si bien es el comportamiento por defecto, es posible user url's amigables en otros sistemas con alguno que otro hack. En wikipedia podremos revisar un artículo más extenso sobre [url's amigables][clean-url] el cual incluye algunos ejemplos.
[^2]: Un slug es un término periodístico que se refiere a los nombres o etiquetas cortas para algo.


[django]: https://djangoproject.com
[design-your-urls]: https://docs.djangoproject.com/en/1.5/intro/overview/#design-your-urls
[django-sql-injection]: https://docs.djangoproject.com/en/1.5/topics/security/#sql-injection-protection
[seo]: https://en.wikipedia.org/wiki/Search_engine_optimization
[dynamic-urls-vs-static-urls]: http://googlewebmastercentral.blogspot.com/2008/09/dynamic-urls-vs-static-urls.html
[usabilidad]: http://es.wikipedia.org/wiki/Usabilidad
[stackoverflow]: http://stackoverflow.com/a/910741/1472750
[clean-url]: https://en.wikipedia.org/wiki/Clean_URL
[django-slugify]: https://docs.djangoproject.com/en/1.5/ref/utils/#django.utils.text.slugify
[django-slugfield]: https://docs.djangoproject.com/en/1.5/ref/models/fields/#slugfield
[django-uuslug]: https://github.com/un33k/django-uuslug