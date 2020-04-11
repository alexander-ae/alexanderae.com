Title: Profiling con Python
Date: 2020-04-12
Tags: python,optimizacion
Slug: profiling-python
Author: __alexander__
Summary: Revisaremos el concepto de profiling, los módulos que podemos utilizar en python (profile, cprofile) asi como el uso de una interfaz gráfica (snakeviz) para ver los resultados.

Hoy tuve como tarea reducir el tiempo de ejecución de una rutina que tomaba 40 minutos. Era código extenso que veía por primera vez, por lo que decidí usar el módulo "cProfile" de python para realizar un análisis de los posibles cuellos de botella y saber *qué se debe tomar como prioridad al optimizar del total del código*.

Finalmente logré alcanzar los 3 minutos de ejecución centrándome solo en los métodos más lentos o aquellos que se llamaban en altas cantidades. 

### ¿A qué se le llama profiling?

Se refiere a la acción de realizar la medición de con qué frecuencia y en cuanto tiempo se ejecutan las diversas partes de un programa.

### Profiling en Python

Python incluye los módulos **cProfile** y **profile** en su librería estandar para realizar profiling.

Ambos módulos proveen las mismas interfaces (métodos) pero la diferencia radica en que *profile* está implementado en python y es más fácil "extenderlo" (personalizarlo).

La documentación nos recomienda utilizar **cProfile**.

### Ejemplo de uso

Para el ejemplo utilizo la serie de Fibonacci:

~~~
::python
import profile

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def fib_seq(n):
    seq = [ ]
    if n > 0:
        seq.extend(fib_seq(n-1))
    seq.append(fib(n))
    return seq

profile.run('print(fib_seq(32))')
~~~

Cuyo resultado es:

~~~
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
18454895/33    4.665    0.000    4.665    0.141 <stdin>:1(fib)
     33/1    0.000    0.000    4.665    4.665 <stdin>:1(fib_seq)
        1    0.000    0.000    4.666    4.666 <string>:1(<module>)
        1    0.000    0.000    4.666    4.666 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
       33    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
       32    0.000    0.000    0.000    0.000 {method 'extend' of 'list' objects}

~~~

Donde tenemos que:

- ncalls: es el total de veces que se llaman a la función. En este caso la función *fib* se llama 18454895 veces debido a que es  una función recursiva.

- tottime: es el total de tiempo que transcurre exclusivamente dentro de la función sin tomar en cuenta las llamadas a subfunciones de la misma.

- percall: es el tiempo anterior pero dividido entre el total de llamadas a la función (tiempo promedio).

- cumtime: es el tiempo total dentro de una función (incluidas subfunciones)

- percall: "cumtime" / número de ejecuciones (tiempo promedio total)

- filename:lineno(function): se refiere a la función en cuestión


Para facilitar el paso de parámetros también podemos utilizar el método **runctx**:

~~~
    cProfile.runctx('fib_seq(n)', globals(), {'n': 32})
~~~

e inclusive podemos generar un archivo que contenga los resultados:

~~~
    cProfile.runctx('fib_seq(n)', globals(), {'n': 32}, 'output.prof')
~~~

### Utilizando snakeviz para visualizar los resultados de forma gráfica

Snakeviz es un visor gráfico basado en el navegador para la salida del profiler "cProfile" de python.

Para instalarlo bastaría:

>   pip install snakeviz

y luego ya solo llamaríamos a la aplicación en consola mediante:

>   snakeviz output.prof

y nos mostrará una salida similar a:

![screenshot of snakeviz](/pictures/snakeviz.png "Profiling - snakeviz")

en la que se desglosan las respectivas funciones llamadas y sus tiempos.

- - -

### Recursos:

- <a target='_blank' href='https://docs.python.org/3.8/library/profile.html'>Python profile</a>: Librería estándar de Python

- <a target='_blank' href='https://pymotw.com/2/profile/'>profile, cProfile, and pstats</a>: Performance analysis of Python programs

- <a target='_blank' href="https://jiffyclub.github.io/snakeviz/">Snakeviz</a>