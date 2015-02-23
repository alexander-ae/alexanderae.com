Title: Memcached
Date: 2013-03-19 22:03
Tags: memcached, optimizacion,
Slug: memcached
Author: __alexander__

[Memcached][memcached] es un sistema distribuido de caché en memoria orientado a objetos.

##### ¿Qué quiere decir?, ¿cuáles son sus características?

- *distribuido*: **memcached** puede instalarse en varios servidores a la vez que pueden ser configurados para actuar como una sola entidad sin comunicarse entre si.

- *en memoria*: mantiene los fragmentos de información en la memoria RAM

- *orientado a objetos*: almacena los items en pares del tipo clave-valor basándose en [tablas hash][tabla-hash]

- *Implementado en el servidor y en el  cliente*: el cliente sabe como enviar items al servidor, cuando no se puede contactar al servidor y como solicitar items del servidor. El servidor sabe como almacenar, retornar o expirar los items según las solicitudes del cliente.

- - -

##### Instalación

Podemos instalarlo mediante el gestor de paquetes de nuestro sistema operativo:

~~~
    apt-get install memcached

    pacman -S memcache

    yum install memcached
~~~


o compilándolo:

~~~~
    wget http://memcached.googlecode.com/files/memcached-1.4.x.tar.gz
    tar xfz memcached-1.4.x.tar.gz
    cd memcached-1.4.x/
    ./configure
    make && make install
~~~~

podemos comprobar la ruta del comando mediante:

~~~
    which memcached
~~~

lo que nos debería retornal algo así como:

~~~
    /usr/local/bin/memcached
~~~

y si algo falla, siempre podemos consultar la [wiki][memcached-wiki].

- - -

##### Ejecución

Podemos ejecutar el comando **memcached** con algunas opciones como:

~~~
    memcached -d -p 11211 -m 128 -c 1024 -P $HOME/memcached.pid
~~~

donde:

- d: permite correr memcached como un [demonio][demonio]
- p: indica el puerto, por defecto es 11211
- m: cantidad de memoria en MB máxima a usar
- c: número máximo de conexiones simultáneas
- P: ubicación del archivo en el que se almacenará el PID del proceso, solo es válido cuando se ejecuta como un demonio.

se puede leer el manual, como siempre, por medio de:

~~~
    man memcached
~~~

Para comprobar que se esté ejecutando, podemos usar telnet, lo que nos devuelve algo como:

~~~
    telnet localhost 11211
    Trying 127.0.0.1...
    Connected to localhost.
~~~

que indica que se ha conectado a memcached por medio del puerto que especificamos.

- - -

##### Memcached y Systemd

Como adicional, el archivo de configuración y scripts necesarios para administrar memcached mediante [systemd][systemd-chakra].

*memcached.config:*

~~~
    PORT="11211"
    USER="user"
    MAXCONN="512"
    CACHESIZE="32"
    PID="/home/user/.memcached.pid"
    OPTIONS=""
~~~

*memcached.service:*

~~~
    [Unit]
    Description=memcached daemon
    After=network.target

    [Service]
    EnvironmentFile=/etc/sysconfig/memcached.config
    ExecStart=/usr/local/bin/memcached -p ${PORT} -u ${USER} -m ${CACHESIZE} -c ${MAXCONN} -P ${PID} $OPTIONS
    ExecStop=/bin/kill -9 'cat ${PID}'; /bin/rm ${PID}

    [Install]
    WantedBy=multi-user.target
~~~

con ello, solo tendríamos que ejecutar, según convenga:

~~~
    systemctl start memcached
    systemctl stop memcached
    systemctl status memcached
~~~

Y con ello, tenemos lista la configuración del servidor de memcached. Lo siguiente es configurar un cliente, y a empezar a usar la caché!

[memcached]: http://memcached.org/
[tabla-hash]: http://es.wikipedia.org/wiki/Tabla_hash
[memcached-wiki]: https://code.google.com/p/memcached/wiki/NewStart
[demonio]: http://es.wikipedia.org/wiki/Demonio_(inform%C3%A1tica)
[systemd-chakra]: http://chakra.sourceforge.net/wiki/index.php/Systemd