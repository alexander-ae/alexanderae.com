Title: Markdown en django
Date: 2013-12-07 10:18
Tags: django, markdown,
Slug: markdown-en-django
Author: __alexander__

Como ya sabemos, a partir de la versión 1.5 de [django][django], el módulo [contrib.markup][contrib.markup] esta siendo depreciado. Por ello, si buscamos incluir markdown en nuestro proyecto debemos recurrir a paquetes de terceros o crear nuestro propio "template filter" (si deseamos escapar markdown como html), lo cual no es tan complicado.

Lo primero a necesitar es un paquete que convierta markdown a html. De los dos que probé [markdown][markdown] y [markdown2][markdown2] me quedo por el primero porque incluye algunas opciones como *output_format*.

Inicialmente nuestro [template filter][django_template_filter] puede lucir más o menos así:

~~~
::python
from django import template
from django.template.defaultfilters import stringfilter
from markdown import markdown

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def mrkdwn(txt):
    return markdown(txt)
~~~

La función **markdown**, entre otros, acepta algunos parámetros como:

- safe_mode: permite deshabilitar html (a pesar del nombre, no es una garantía de ser un *modo seguro*)
- html_replacement_text: texto a mostrar cuando safe_mode toma el valor de *replace*
- enable_attributes: controla la conversión de atributos html (desactivado cuando safe_mode vale *True*)

entre [otras][markdown-docs]

Y si el código markdown será ingresado por usuarios no confiables[^1], debemos tener en cuenta que podría insertarse código malicioso.

Podríamos mejorar un tanto la primera versión de nuestro filtro:

~~~
::python
from django import template
from django.template.defaultfilters import stringfilter
from markdown import markdown

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def mrkdwn(txt):
    return markdown(txt, safe_mode=True, output_format='html5',
        enable_attributes=False)
~~~

- - -

Este es el template html con el que hice mis pruebas:

~~~
::jinja

{% load my_tags %}

<h1>Test</h1>

{{ 'hola'|mrkdwn }}
<br>
{{ 'áéíóúñ'|mrkdwn }}
<br>
{{ '<b>bold</b>'|mrkdwn }}
<br>
{{ 5|mrkdwn }}
<br>
{{ '**test** <b>otro test</b>'|mrkdwn }}
<br>
{{ '*cursiva<b>bold</b>*'|mrkdwn }}
<br>
{{ '{@onclick=alert("hi")}es en serio?'|mrkdwn }}
<br>
~~~

Posiblemente la última versión que utilicé tampoco sea del todo segura, se pueden ver algunas discusiones sobre el tema aquí:

- [Best practice for allowing Markdown in Python, while preventing XSS attacks](http://stackoverflow.com/a/5359237/1472750)
- [How do I use Markdown securely?](http://security.stackexchange.com/a/14674)

Y como decía *Gene Spafford*:

> El único sistema realmente seguro es aquel que está apagado, confinado en un bloque de hormigón y sellado en una habitación forrada de plomo con guardias armados – y aún así tengo mis dudas.


[^1]: en un sistema de comentarios por ejemplo


[django]: https://docs.djangoproject.com/
[contrib.markup]: https://docs.djangoproject.com/en/dev/releases/1.5/#django-contrib-markup
[markdown]:https://pypi.python.org/pypi/Markdown
[markdown2]: https://pypi.python.org/pypi/markdown2
[django_template_filter]: https://docs.djangoproject.com/en/dev/howto/custom-template-tags/
[markdown-docs]: http://pythonhosted.org/Markdown/reference.html