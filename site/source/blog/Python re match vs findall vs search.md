Title: Python: match vs findall vs search
Date: 2014-01-26
Tags: python, regexp
Slug: python-match-vs-findall-vs-search
Author: __alexander__

En el último par de semanas tuve que desarrollar un sistema web que interactuase con dispositivos GPS [^1].

Uno de los módulos que implementé consistía en una función que tenia que parsear[^2] los SMS recibidos, ya que estos eran el medio por el que el dispositivo retornaba los resultados.

De manera resumida, el proceso que seguía era:

1. Recibir el SMS
2. Comprobar si el SMS coincide con alguna de las expresiones regulares almacenadas
3. Si se encuentra alguna coincidencia, se debe ejecutar algun procedimiento en particular según el tipo de mensaje recibido.

- - -
A modo de ejemplo, muestro 2 de las expresiones regulares que utilicé:

> ^begin ok

> ^Latitude:(?P<lat>[\d\.SN]+)([\s]+)Longitude:(?P<lon>[\d\.WE]+)([\s]+)

La primera es la respuesta entregada al inicializar un dispositivo, mientras que la segunda se corresponde a una versión resumida del formato en el que se nos retorna la posición.

Para saber si uno de los mensajes cumple con algunas de las expresiones regulares podríamos usar los métodos  [search][re-search], [match][re-match] o [findall][re-findall].

Los 3 métodos los podemos usar dentro de una sentencia *if* para saber si se encuentra o no, una coincidencia. Entonces, si por ejemplo tenemos el siguiente SMS:

> Latitude:12.013001S Longitude:077.079241W

podríamos escribir algo como:

~~~
::python

import re

regex_BEGIN = re.compile('^begin ok')
regex_POSITION = re.compile('^Latitude:(?P<lat>[\d\.SN]+)([\s]+)Longitude:(?P<lon>[\d\.WE]+)([\s]+)')

msg = 'Latitude:12.013001S Longitude:077.079241W' # mensaje para este ejemplo

if regex_BEGIN.match(msg):
    print 'Dispositivo inicializado'

if regex_POSITION.match(msg):
    print 'Lectura de la posicion'

~~~

El código anterior lo podríamos reescribir cambiando el *match* por un *search* [^3]. Entonces, me pregunté cuál de los tres métodos podría ser la diferencia entre los tiempos de ejecución de estos 3 métodos.

Usando timeit para medir tiempos, mi script indicando los tiempos obtenidos debajo de cada sentencia fue:

~~~
::python
import timeit

# Primera prueba

setup = '''
import re
s = 'Latitude:12.013001S Longitude:077.079241W'
r = re.compile('^Latitude:(?P<lat>[\d\.SN]+)([\s]+)Longitude:(?P<lon>[\d\.WE]+)')
'''
print timeit.timeit(stmt="r.match(s)", setup=setup, number=1000000)
# 1.20556092262

print timeit.timeit(stmt="r.search(s)", setup=setup, number=1000000)
# 1.18701195717

print timeit.timeit(stmt="r.findall(s)",  setup=setup,  number=1000000)
# 1.58948493004

print '- - -'

# Segunda prueba

setup = '''
import re
s = 'Latitude:12.013001S Longitude:077.079241W'*100
r = re.compile('^Latitude:(?P<lat>[\d\.SN]+)([\s]+)Longitude:(?P<lon>[\d\.WE]+)')
'''

print timeit.timeit(stmt="r.match(s)", setup=setup, number=1000000)
# 1.18745613098

print timeit.timeit(stmt="r.search(s)", setup=setup,  number=1000000)
# 1.19270586967

print timeit.timeit(stmt="r.findall(s)", setup=setup, number=1000000)
# 49.8060359955

print '- - -'

# Tercera prueba

setup = '''
import re
s = 'Latitude'*100
r = re.compile('Latitude')
'''
print timeit.timeit(stmt="r.match(s)", setup=setup, number=1000000)
# 0.517388105392

print timeit.timeit(stmt="r.search(s)", setup=setup, number=1000000)
# 0.369539022446

print timeit.timeit(stmt="r.findall(s)", setup=setup, number=1000000)
# 11.6244080067

~~~

##### Conclusiones

En los 9 casos realicé un millón iteraciones para que la diferencia entre cada método sea notable, por lo que si tan solo tuviera que realizar 1 iteración, posiblemente no habría mucha diferencia entre el método escogido.

Si bien se observan mejores tiempos con los métodos *match* y *search*, debido a que hay muchos factores que afectan el tiempo de ejecución, recomendaría que cada uno evaluase el método que mejor se adapte a sus necesidades, aunque como mencioné, posiblemente para casos simples, esto no sería un motivo de preocupación.

Siempre recordando que:

> " La optimización prematura es la raíz de todos los males"  *Donald Knuth*

###### Referencias:

- [re.match vs re.search performance difference][ref_1]
- [What's a faster operation, re.match/search or str.find?][ref_2]

[^1]: De aquellos que se instalan en vehículos motorizados.
[^2]: Analizar una cadena de texto para interpretar su contenido.
[^3]: Inclusive por un findall u algún otro método.

[re-search]: http://docs.python.org/2/library/re.html#re.search
[re-match]: http://docs.python.org/2/library/re.html#re.match
[re-findall]: http://docs.python.org/2/library/re.html#re.findall

[ref_1]: http://stackoverflow.com/questions/12803709/
[ref_2]: http://stackoverflow.com/questions/4901523