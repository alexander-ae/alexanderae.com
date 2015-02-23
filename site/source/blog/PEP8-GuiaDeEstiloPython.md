Title: PEP 8 - Guía de Estilo para Python
Date: 2013-03-03 17:56
Tags: python, desarrollo-de-software,
Slug: pep8-guia-de-estilo-para-python
Author: __alexander__

Desde que empezamos[^1] a escribir código y conforme progresamos, adquirimos ciertas pautas que definen la manera en que expresamos nuestras ideas en el lenguaje que manejemos, ya sea javascript, python, html u otro. Esto define nuestro *estilo*, y toma en cuenta la manera en la que indentamos[^2], definimos nombres de variables y funciones, el proceso de realizar o no comentarios de codigo entre otros.

<br>
##### ¿Por qué es importante adoptar un estilo?

Por muchos motivos:

Es probable que el código deba ser mantenido, ya sea por nosotros u otras personas:

En caso de que seamos nosotros los responsables, no recordaremos por siempre que hacia tal o cual función o para que implementamos alguna clase. El solo hecho de añadir comentarios, mantener un orden de los métodos, clases y funciones, indentar y lo más importante: *el haber sido consistentes*  puede ayudar en gran medida.

Al trabajar en equipo esto se hace mucho más notorio. Si todos los miembros siguen unas líneas generales, aunque no se conozca con exactitud el "que hace" de algún bloque de código, al seguir un estilo el proyecto se hace legible y permite que el *"dolor"* al revisarlo sea menor.

*¿Qué sucede cuando tienes que revisar código ajeno y observas inconsistencias en el estilo del código?*

Puede que tengas que revisar el archivo operaciones.py y te encuentres con algo como:

~~~~
::python
def suma(a,b):
  a=int(a) #convierto la variable 'a' a entero
  b = int(b) #convierto la variable 'b' a entero
  return   (a+ b)

def resta( c , d):
    c = int(c)
    d = int(d)
    return c-d

def multiplica(e,f):
    return ( int( e ) * int( f ) )
~~~~

aunque podría haber sido peor[^3], a primera vista me parecería que el que escribiera algo así, es *inconsistente*.

- ¿Era necesario incluir los comentarios?
- Mientras en la función suma se indentó con 2 espacios, en las funciones siguientes se usaron.
- El espaciado entre variables y operadores tambien cambia según avanzamos.
- Inclusive la forma en la que definimos a las funciones, tanto para *suma* y *resta*, convertimos las variables a enteros en una línea aparte; pero para la multiplicación, lo hicimos todo en una sola ĺínea.

*¿Por donde comenzar?*

Como siempre, no tenemos que inventar algún estándar para nuestro grupo de trabajo o para nosotros mismos[^4], es muy probable que ya exista alguna convención para nuestro lenguaje preferido y tan solo debamos de revisarla y adoptarla[^5], por ejemplo:

- CSS: [guia de estilos para css de github][github-css]
- HTML - CSS: [guia de estilos para html y css de google][google-html-css]
- Javascript: [guia de estilos para javascript de jquery][jquery-js]
- Ruby: [guia de estilos para ruby][ruby-styleguide]

<br>
##### PEP 8
En python existe lo que se llaman PEP's o *Python Enhancement Proposals*[^6], una de las cuales, PEP 8[^7] está dedicada a la recopilación de los estándares seguidos por los desarrolladores de python a la hora de escribir código python para la librería estandar.

Entre las convenciones principales, tenemos:

- *Usar 4 espacios para indentar*

- Es posible usar solo tabulaciones u ocho espacios para código antiguo que haya sido escrito así. *Por ningún motivo se han de mezclar espacios y tabulaciones*.

- Limitar los tamaños de línea a *79 caracteres como máximo*, si bien se puede continuar líneas largas con el símbolo '*\\*', es recomendable el uso de paréntesis, por ejemplo en vez de:

~~~~
::python
def __init__(self, first, second, third, fourth, fifth, sixth):
    output = first + second + third + fourth \
        + fifth + sixth
~~~~

podríamos hacer uso de los paréntesis:

~~~~
::python
def __init__(self, first, second, third, fourth, fifth, sixth):
    output = (first + second + third + fourth
        + fifth + sixth)
~~~~

- Se deben separ las funciones de nivel superior y las clases con dos líneas en blanco, mientras que los métodos dentro de clases los podemos separar con una sola línea. También se pueden usar líneas en blanco dentro de las funciones para separ bloques que guardan cierta correlación lógica.

- Las sentencias de *import* deben de estar generalmente separadas una en cada línea, por ejemplo:

~~~~
::python
Incorrecto: import os, sys
Correcto:   import os
            import sys
Se permite: from urllib2 import urlopen, Request
~~~~

- Las sentencias *import* deben de estar siempre en la parte superior del archivo agrupadas de la siguiente manera:
    - Libreria estándar
    - Librerías de terceros
    - import's de la aplicación local

- Usar espacios alrededor de los operadores aritméticos

- *No usar espacios alrededor del signo igual cuando se encuentre en un listado de argumentos de una función*:

~~~~
::python
Incorrecto: def suma(a = 0, b = 0):
Correcto:   def suma(a=0, b=0):
~~~~

- Los comentarios que contradicen al código son *peores* que cuando no existen comentarios!

- No se deben de realizar comentarios obvios

- No se deben comparar booleanos mediante *==*:
~~~~
::python
Incorrecto: if valido == True:
                pass
Correcto:   if valido:
                pass
~~~~

Pueden observar la lista completa en las referencias y como adicional:

1. [¿Por qué el estilo de Programación importa?][why-coding-style-matters]: un artículo en inglés de smashing magazine.
2. [Code Like a Pythonista][pythonista]: Presentación en la que se dan varios tips para programar en python, incluidos algunos ya vistos en el PEP8.


[^1]: Y no digo: 'desde que aprendimos', porque el aprendizaje es continuo y nunca terminamos de aprender.

[^2]: considerando que indenten.

[^3]: algún extremista (nótese que no me refiero a mí) podría recomendar el enviar a la hoguera al que escribio aquello.

[^4]: aunque se puede hacer si le dedicamos el esfuerzo necesario.

[^5]: lo que no significa que sigamos la convención con los ojos cerrados y sin dudar, lo correcto sería extraer las partes que creamos convenientes y aplicarlas. Aunque si estamos iniciando, lo recomendable es seguir las normas y con la experiencia, opinar si debemos o no seguirlas.

[^6]: son documentos que proveen información a la comunidad de python o describen nuevas carácterísticas de python, su proceso de desarrollo o su entorno. más información [aquí][peps]. Y un listado alternativo de los peps [aquí][peps-io]

[^7]: pep8 en [inglés][pep8] y una versión traducida al [español][pep8-español] por Raúl González Duque.


[peps]: http://www.python.org/dev/peps/pep-0001/#what-is-a-pep
[github-css]: https://github.com/styleguide/css
[google-html-css]: http://google-styleguide.googlecode.com/svn/trunk/htmlcssguide.xml
[jquery-js]: http://contribute.jquery.org/style-guide/js/
[ruby-styleguide]: https://github.com/bbatsov/ruby-style-guide
[peps-io]: http://www.peps.io/
[pep8]: http://www.python.org/dev/peps/pep-0008/
[pep8-español]: http://mundogeek.net/traducciones/guia-estilo-python.htm
[why-coding-style-matters]: http://coding.smashingmagazine.com/2012/10/25/why-coding-style-matters/
[pythonista]: http://python.net/~goodger/projects/pycon/2007/idiomatic/presentation.html