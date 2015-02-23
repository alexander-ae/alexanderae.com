Title: Una Historia de Caché
Date: 2013-03-17 12:20
Tags: memcached, optimizacion, base-de-datos,
Slug: una-historia-de-cache
Author: __alexander__

Dos valerosos aventureros, un desarrollador de software y un administrador de sistemas, emprendieron un viaje.
Ellos hacen sitios web. Sitios con servidores web y bases de datos. Los usuarios de todo el internet interactuan con los servidores web y les piden que hagan páginas para ellos. Los servidores web consultan a las bases de datos por la información necesaria para construir las páginas. El desarrollador escribe código y el admininistrador añade servidores web y servidores de base de datos.

Un dia, el administrador se dio cuenta de que su base de datos estaba enferma! Vomitando bilis y materia roja por todas partes! El administrador notó que tenía fiebre, una carga promedio del 20%!

El desarrollador le consulta al administrador: "bueno, ¿qué podemos hacer?".
El administrador responde: "He oído acerca de una gran herramienta llamada [**memcached**][memcached]. Realmente ayudó a LiveJournal".

"Esta bien, probémosla" dice el desarrollador.

Nuestro valeroso administrador observa sus servidores web, de los cuales tiene seis. Decide usar tres de ellos para correr el servidor de memcached. El administrador añade un gigabyte de RAM para cada servidor, e inicia el servidor de memcached con un límite de 1GB cada uno. Entonces, consigue tres instancias de memcached, cada una de las cuales puede almacenar hasta 1GB de datos. Entonces el desarrollador y el administrador retroceden un paso y admiran su glorioso *memcached*!

"¿Ahora qué?" dicen, "no esta haciendo NADA!". Las instancias de memcached no estan interactuando con nada y ciertamente no tienen ningun dato. Y ahora la base de datos tiene una carga del 25%!

Nuestro aventuroso desarrollador coge el manual de la libreria del cliente de *pecl/memcached*, el cual nuestro valeroso adminitrador ayudó amablemente a instalar sobre los seis servidores web.
"No temas", él dice. "Tengo una gran idea!". Él toma las direcciones IP y los números de puertos de las 3 instancias de memcached y las añade a un array en php.

~~~
::html-php
$MEMCACHE_SERVERS = array(
    "10.1.1.1", //web1
    "10.1.1.2", //web2
    "10.1.1.3", //web3
);
~~~

Entonces el hace un objeto, al cual ingeniósamente llama '$memcache'.

~~~
::html-php
$memcache = new Memcache();
foreach($MEMCACHE_SERVERS as $server){
    $memcache->addServer ( $server );
}
~~~

Ahora el desarrollador piensa. Él piensa y piensa y piensa. "Lo tengo!", dice.
"Hay una sección en la página inicial que corre un SELECT * FROM InmensaTabla WHERE timestamp> lastweek ORDER BY timestamp ASC LIMIT 50000; y esto toma cinco segundos". "POngámoslo en memcached". Entonces él envuelve su código para el SELECT y usa un objeto de memcached. Su código consulta:

Están los resultados de este SELECT en memcached?. Si no lo están, ejecuta la consulta, toma los resultados y AÑÁDELOS a memcached! . Algo como esto:


~~~
::html-php
$huge_data_for_front_page = $memcache->get("huge_data_for_front_page");
if($huge_data_for_front_page === false){
    $huge_data_for_front_page = array();
    $sql = "SELECT * FROM hugetable WHERE timestamp > lastweek ORDER BY timestamp ASC LIMIT 50000";
    $res = mysql_query($sql, $mysql_connection);
    while($rec = mysql_fetch_assoc($res)){
        $huge_data_for_frong_page[] = $rec;
    }
    // cache para 10 minutos
    $memcache->set("huge_data_for_front_page", $huge_data_for_front_page, 0, 600);
}

// use $huge_data_for_front_page como desee
~~~

El desarrollador escribe código. El administrador transpira. BAM! . La carga de la base de datos ha bajado al 10%. El sitio web está muy rápido ahora. Ahora el administrador desconcertado, se pregunta. "¿Qué DEMONIOS ha pasado?". "He puesto gráficos en los servidores de memcached! He usado [**cacti**][cacti], y esto es lo que veo! El tráfico se dirige hacia una de las instancias de memcached, pero hice tres :(". Entonces, el administrador rápidamente aprende el protocolo ascii y realiza el comando *telnet* hacia el puerto 11211 sobre cada instancia y se pregunta:

¿Hey, 'get huge_data_for_front_page' estas allí?

La primera instancia no responde ...

La segunda instancia no responde ...

La tercera sin embargo, retorna una gran cantidad de datos en su sesión de telnet! Allí están los datos! Solo una de las instancias tiene la clave de la cache que el desarrollador creó.

Intrigado, consulta en la lista de correo. Ellos responden al unísono, "Es un sistema distribuido de caché! Es lo que hace!". Pero ¿qué es lo que significa?. Aún confundido y un poco asustado por su vida, el administrador le consulta al desarrollador si es posible añadir a la caché algunas cosas más. "Veamos que sucede. Somos gente curiosa", dice el administrador.

"Bueno, hay otro query que no es lento, pero se ejecuta 100 veces por segundo. Tal vez nos pueda ayudar", dice el desarrollador. Entonces el envuelve el código como lo hizo antes. Efectivamente, la carga del servidor se reduce a un 8%! .

Entonces el desarrollador escribé más y más código sobre cosas que pueden ser añadidas a la caché. El usa nuevas técnicas. "Encontré esto en la lista de correos y en la sección de preguntas frecuente", dice.
La carga de la base de datos baja: 7%, 5% , 3%, 2%, 1%!

"Esta bien", dice el administrador de sistemas, "probemos de nuevo!". Ahora el observa los gráficos. TODAS las instancias de memcached estan corriendo! Todas estan recibiendo pedidos! Esto es genial! Todas son usadas!

Entonces nuevamente, el toma las llaves que el desarrollador usó y las observa en los servidores de memcached. 'get this_key' 'get that_key'. Pero cada vez que el lo hace, solo la encuentra sobre una de las instancias! . Ahora ¿POR QUÉ debería suceder esto? piensa él. Y pasa toda la noche intrigado. Qué tonto! ¿No deseas que todas las llaves esten en todas las instancias?

"Pero, espera", el piensa, "Le otorgué a cada instancia de memcached 1 gigabyte de memoria, eso significa, que en total, puedo tener en caché hasta TRES gigabytes de mi base de datos, en vez de solo UNA!". "Esto es grandioso!", piensa. "Esto me ahorrará una tonelada de dinero". Brad Fitzpatrick te amo! .

"Pero .., el siguiente problema es otra cosa que me desconcierta, este servidor web que tengo aquí y esta corriendo una instancia de memcached es viejo, esta enfermo y necesita ser actualizado. Pero para hacerlo, tengo que apagarlo! ¿Qué le pasará a mi pobre cluster de memcached?. Averigüémoslo" dice él, y apaga el servidor. Ahora observa sus gráficos. "Oh, no, la carga de la bbdd, ha subido. Ya no es de 1%, es del 2%, pero aun es tolerable". Todas las demás instancias aún reciben tráfico. Entonces devolvamos el servidor de vuelta, y pongamos a memcached de vuelta al trabajo. Después de unos minutos, la carga de la bbdd vuelve nuevamente a bajar al 1%, donde debería estar".

"La caché se restauró a si misma! Ahora lo entiendo. Si no está disponible, solo significa que algunas de mis peticiones se perdieron. Pero no es suficiente como para matarme. Eso es muy dulce".

Entonces el desarrollador de software y el administrador de sistemas continuaron construyendo sitios web. Ellos continuaron usando la caché. Cuando tienen dudas consultan la lista de correos o leen las preguntas frecuentes nuevamente. Ellos observan sus gráficos. *Y todos vivieronn felices para siempre.*


Autor: [Dormando][dormando] via IRC. Editado por Brian Moon. Edición adicional por Emufarmers.

Esta historia ha sido ilustrada por el comic online [TOBlender.com][TOBlender]

- - -

Encontré esta historia mientras revisaba la [wiki][wiki-memcached] de *memcached*. Me gustó tanto que me animé a realizar la traducción anterior, la cual por cierto tal vez no sea fiel a la original, pero hice mi mejor intento!

[memcached]: http://memcached.org/
[livejournal]: http://www.livejournal.com/
[cacti]: http://www.cacti.net/
[dormando]: https://twitter.com/dormando
[TOBlender]: http://toblender.com/tag/memcached/
[wiki-memcached]: https://code.google.com/p/memcached/wiki/TutorialCachingStory