Title: Django: procesamiento condicional de vistas
Date: 2014-04-19
Tags: django, optimizacion
Slug: django-procesamiento-condicional-de-vistas
Author: __alexander__

¿Qué pasá cuando un cliente en su afán por estar siempre al día, comienza a presionar la tecla de actualizar el navegador repetidas veces ?

Y siendo aún más pesimistas (o tal vez realistas), ¿qué pasa si varios clientes realizan la misma acción una y otra vez posiblemente para ser los primeros en leer una noticia?

Sucedería que nuestro servidor enviaría una y otra vez el mismo contenido, consumiendo ancho de banda, sin importar que nuestra página no tenga contenido nuevo o actualizado.

<br>

### Etags y Last Modified:

Existen dos maneras de indicarle al cliente que nuestro contenido no ha cambiado:

- [**Etags**][etag]: Son identificadores asignados al contenido de un recurso solicitado. Se utilizan para descubrir si el contenido en cuestión ha cambiado o no.

- [**Last Modified**][last-modified]: Esta cabecera nos brinda la fecha de la última modificación de un recurso, con lo que podriamos realizar un condicional para buscar algun cambio con respecto al contenido que ya disponíamos en caché.

<br>

### Django y el procesamiento condicional de vistas

Django incorpora algunas herramientas para facilitarnos esta tarea. Estas son:


*1.* **El decorador condition**: Recibe dos parámetros opcionales los cuales representan a las funciones de cálculo del etag y el atributo last_modified.

Por ejemplo, para una aplicación del tipo blog, que debe retornar contenido solo si la publicación se ha actualizado (en base al atributo modified):

~~~
::python

# models.py

class Publicacion(models.Model):
    modified = models.DateTimeField('Ultima mod.', auto_now=True)
    titulo = models.CharField('Titulo', max_length=120)
    slug = models.CharField('Slug', max_length=160)
    ...

# views.py
...
from django.views.decorators.http import condition

def detalle_last_mod(request, slug):
    ''' Calcula el valor de last_modified '''
    return Publicacion.objects.get(slug=slug).modified


@condition(last_modified_func=detalle_last_mod)
def detalle(request, slug=''):
    ''' Vista que retorna una publicación '''
    p = Publicacion.objects.get(slug=slug)

    return render('publicacion.html', locals(),
                  context_instance=ctx(request))
~~~

Para el ejemplo, creé un proyecto de prueba y cargué una publicación en el navegador por primera vez:

![request-1][request-1]

Como se puede observar en los *headers* del *request*, todo está normal. Pero en el *response*, hemos obtenido una cabecera que indica la fecha del last-modified.

Entonces, si ejecutamos un nuevo request:

![request-2][request-2]

podemos observar que en el *request* se añadió una cabecera que dice *if-modified-since* que básicamente se pregunta si la página fue actualizada desde la última fecha que recibimos.

Y debido a que para mi ejemplo, no realicé ninguna modificación, recibimos el estado *304* que es un *NOT MODIFIED*, así como también el mismo parámetro last-modified.

<br>

*2.* **Los decoradores @etag y @last_modified**: Similares al método anterior, pero estos se concentran en solo una de las dos funciones (etag o last-modified).

Por ejemplo:

~~~
::python
@etag(etag_func)
def detalle(request, slug=''):
    ...
~~~

<br>

*3.* **Middleware de procesamiento condicional** (middleware conditional processing): django incorpora también un middleware que genera etags de manera automática para *todas* nuestras vistas, considerando que:

- Se aplica a todas las vistas
- Para calcular el valor del *etag*, se basa en el *response* generado por nuestra vista, por lo que si calcular nuestros *response* son acciones "pesadas", tal vez nos convenga usar uno de los dos primeros métodos antes indicados.
- Solo son apropiados para pedidos del tipo *GET* (no he probado si se refiere a que ignora otros métodos o si es que si nosotros usamos otros métodos, no deberíamos usar este método).

- - -

Como siempre, para mayor información, nada como la [documentación oficial][docs].



[etag]: http://en.wikipedia.org/wiki/HTTP_ETag
[last-modified]: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.29
[docs]: https://docs.djangoproject.com/en/1.6/topics/conditional-view-processing/

[request-1]: /pictures/django-conditional-1.png 'Request 01'
[request-2]: /pictures/django-conditional-2.png 'Request 02'