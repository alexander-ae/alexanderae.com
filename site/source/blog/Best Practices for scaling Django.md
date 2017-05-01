Title: Buenas prácticas para escalar Django
Date: 2016-07-16
Tags: django
Slug: django-best-practices
Author: __alexander__
Summary: Mi resumen de una de las conferencias brindadas en la DjangoCon Europa 2016. Anton Pirker nos introduce en la historia (ficticia) sobre el cómo aparece un problema para escalar un nuevo proyecto con django en la vida real de un desarrollador que no tiene experiencia en la administración de servidores.


Mi resumen de una de las conferencias brindadas en la DjangoCon Europa 2016. [Anton Pirker][anton-pirker] nos introduce en la historia (ficticia) sobre el cómo aparece un problema para escalar un nuevo proyecto con django en la *vida real* de un desarrollador que no tiene experiencia en la administración de servidores.

Para quien cuente con tiempo, le recomiendo que revise el video original, el cual está al al final de esta entrada (25 minutos). Pero para quien solo tenga unos minutos, aquí va mi resumen.

- - -

Anton comienza introduciendo al equipo:

Betty, desarrolladora web con experiencia en django y Marissa con el perfil administrativo.

![team][team-img]

Luego nos describe el stack actual del proyecto:

![estructura del proyecto inicial][stack-img]

como se observa, tenemos *nginx* como servidor web, *gunicorn* como servidor python y *postgresql* como servidor de base de datos.

Se nos muestra que el sitio web, ya en producción, comienza a tener problemas, anda un poco lento. Betty decide investigar y descubre [django debug toolbar][django-debug-toolbar]. Con ello observa lo siguiente:
 
> El sitio web está realizando 1292 querys en un tiempo de 813 ms (relativo, claro, a la pc al ordenador en que se realizan pruebas).

Betty investiga que una de las maneras para reducir el número de querys es mediante [select related][select_related] y [prefetch related][prefetch_related]. Con lo que después de una nueva medición, llega a:
 
> 201 querys y 136 ms bajo las mismas condiciones

Este es un primer logro, por lo que decide monitorizar el servidor para saber qué sucede en él.

- - -

Escucha sobre [New Relic][new-relic], un servicio de monitorización de servidores con lo que observa las siguientes estadísticas:

> server 1: 99.3% cpu, 99.6% disk , 91.6% memory

Con ello decide cambiar a 2 servidores y las nuevas estadísticas son:

> server 1: 73.4% cpu , 49.3% disk , 80.8% memory
> db1     : 58.2% cpu , 54.3% disk , 55.6% memory

Siempre se debe monitorear los servidores para saber qué está pasando.

- - -

Betty sigue avanzando, esta vez desea experimentar con la cache, por lo que decide probar [memcached][memcached]. Memcached es un sistema que almacena objetos en memoria para ser accedidos de manera más eficiente.

![memcached][memcached-img]

Entonces, decide colocar un comentario en el html para saber en qué momento se está generando la página y observa algo como lo siguiente:

![memcached-fail][memcached-fail-img]

El problema es que observa que la fecha-hora de generación de las páginas siempre cambia. Esto significa que la cache no está trabajando como debería.

Luego de investigar un poco, concluye que es por las cookies. Por lo que decide removerlas.

- - -

Luego, sucede un error. Al parecer todos los usuario observan lo mismo, todos son *Gina Caputo*:

![memcached-same-user][memcached-same-user-img]

Entonces, la expresión de Betty, al comprender la causa, es similar a:

![fail][fail-img]

Y Marissa, bueno.. ya se imaginarán.

Betty investiga a fondo y después de un tiempo, leyendo sobre cómo funciona la cache, los middlewares de django y demás, logra solucionar el problema.

- - -

Despues de un fin de semana tranquilo, aparece otro error. Cada cierto tiempo, los usuarios observan :

![database error][database-error]

y el log indica:

![database log][database-log]

El error es causado porque el servidor de base de datos agota las conexiones. Entonces, decide utilizar [pg bouncer][pg-bouncer], un gestor de conexiones para postgresql. Ahora si, parece que se ha vuelto una experta en bases de datos.

- - -
Y por fin tiene tiempo para investigar lo que siempre quiso, procesos asíncronos.

![async][async]

Lee sobre [celery][celery]. Celery trabaja mediante "workers", los cuales procesan las tareas que están almacenada en una cola(queue) que Django va añadiendo.
También aprende que debe utilizar un almacen de base de datos, por lo que investiga sobre [redis][redis].

Luego implementa [flower][flower], una herramienta para monitorizar celery, con lo que el stack finalmente queda similar a:

![final stack][final-stack]

y por fin logra el **Level 2** como desarroladora:

![level 2 de 800][level2]

Con ello finaliza la charla, salvo por algunas preguntas de los espectadores.

- - -

Entre mis conclusiones, podría decir que se nos ha mostrado que llevar un proyecto a producción puede ser mucho más complicado de lo esperado. Puede requerir un esfuerzo colosal si no tenemos experiencia manejando servidores.

Pero, como siempre, nadie comienza sabiendo todo y poco a poco, se pueden ir añadiendo componentes según se necesiten.

- - -

Adjunto el video original:

<div class='responsive-embed-youtube'> 
    <iframe class='video' width="560" height="315" src="https://www.youtube.com/embed/Ul-pHtOfA9U" frameborder="0" allowfullscreen></iframe>
</div>

Y los slides en [slides.com][slides].

[team-img]: /pictures/best-practices-for-scaling-django/1-team.png 'the team'
[stack-img]: /pictures/best-practices-for-scaling-django/2-stack.png 'estructura inicial del proyecto'
[memcached-img]: /pictures/best-practices-for-scaling-django/3-memcached.png 'memcached'
[memcached-fail-img]: /pictures/best-practices-for-scaling-django/3-memcached-fail.png 'memcached html'
[memcached-same-user-img]: /pictures/best-practices-for-scaling-django/4-same-user.png 'same user'
[fail-img]: /pictures/best-practices-for-scaling-django/5-fail.png 'fail'
[database-error]: /pictures/best-practices-for-scaling-django/6-database-error.png 'database error'
[database-log]: /pictures/best-practices-for-scaling-django/7-log.png 'database log'
[async]: /pictures/best-practices-for-scaling-django/8-async.png 'async'
[final-stack]: /pictures/best-practices-for-scaling-django/9-final.png 'final stack'
[level2]: /pictures/best-practices-for-scaling-django/10-level-2.png 'level 2'

[anton-pirker]: http://www.anton-pirker.at/
[django-debug-toolbar]: https://github.com/django-debug-toolbar/django-debug-toolbar
[select_related]: https://docs.djangoproject.com/es/1.9/ref/models/querysets/#select-related
[prefetch_related]: https://docs.djangoproject.com/es/1.9/ref/models/querysets/#prefetch-related
[new-relic]: https://newrelic.com/
[memcached]: https://memcached.org/
[pg-bouncer]: https://pgbouncer.github.io/
[celery]: http://www.celeryproject.org/
[redis]: http://redis.io/
[flower]: http://flower.readthedocs.io/en/latest/
[slides]: http://slides.com/antonpirker/best-practicesforscaling-django
