Title: Supervisor
Date: 2013-05-28
Tags: sysadmin, linux
Slug: supervisor
Author: __alexander__

[Supervisor][supervisor] es un sistema del tipo cliente/servidor que nos facilita la administración de procesos en sistemas tipo unix.

Consta de 2 componentes:

supervisord
  : Es quien actua como servidor y se encarga de iniciar los programas asociados, asi como responder a las peticiones de comandos de los clientes y reiniciar subprocesos crasheados o terminados.
  Utiliza un archivo de configuración el cual por defecto reside en */etc/supervisord.conf*


supervisorctl
  : Es por medio de quien el usuario interactua con supervisord. Con él, es posible obtener el estado, detener o iniciar los subprocesos administrados.

- - -

##### Instalación y uso

Lo [instalamos][supervisor-install] con:

    sudo pip install supervisor

Supervisor utiliza un archivo que contiene sus parámetros de configuración, por defecto ubicado en */etc/supervisord.conf*.
En caso de que no exista o deseemos copiar el archivo por defecto para utilizarlo desde otra ubicación, podemos ejecutar:

    echo_supervisord_conf > /etc/supervisord.conf

El archivo de configuración luce similar a:

        [unix_http_server]
        file=/tmp/supervisor.sock   ;

        [supervisord]
        logfile=/tmp/supervisord.log ;
        logfile_maxbytes=50MB        ;
        logfile_backups=10           ;
        loglevel=info                ;
        pidfile=/tmp/supervisord.pid ;

        [supervisorctl]
        serverurl=unix:///tmp/supervisor.sock ;

        [rpcinterface:supervisor]
        supervisor.rpcinterface_factory=supervisor.rpcinterface:make_main_rpcinterface

y, para cada aplicación a controlar debemos añadir una sección *[program:program-name]*, como por ejemplo:

        [program:mongodb]
        directory=/home/username/apps/mongodb-linux-x86_64-2.2.3 
        command=/usr/bin/mongod --dbpath /home/username/apps/mongodb-linux-x86_64-2.2.3/data --logpath /home/username/apps/mongodb-linux-x86_64-2.2.3/log/mongodb.log --config /etc/mongodb.conf --logappend --auth
        autorestart=true

- - -

El ejemplo anterior añade una entrada de configuración para [mongodb][mongodb], se pueden ver otros ejemplos [aquí][supervisor-examples].

Entonces, podemos iniciar supervisor mediante:

    supervisord

y administrar los procesos con *supervisorctl*, usando mongodb como ejemplo:

- Listar: supervisorctl
- Iniciar: supervisorctl start mongodb
- Detener: supervisorctl stop mongodb
- Reiniciar: supervisorctl restart mongodb

En nuestro ejemplo, si iniciamos mongod con *supervisor* y luego obtenemos su PID (id del proceso)

    ps -aux|grep mongod

para poder terminarlo manualmente (asumiendo que su PID sea 2871):

    kill 2871

observaremos que debido a que configuramos la entrada *[program:]* con el valor de *autorestart=true*, **supervisor** se encargará de reiniciar nuestro proceso automaticamente (lo podemos comprobar volviendo a realizar un filtro de los procesos activos).

Con lo cual ya tenemos varios excelentes motivos por los que usar esta herramienta.

- - -

Algunos buenos artículos sobre supervisor que encontré son:

- [How to install and configure Supervisord][articulo-1]: Instalación y configuración básica
- [Managing site processes with Supervisord][articulo-2]: 
- [Daemon Showdown: Upstart vs. Runit vs. Systemd vs. Circus vs. God][articulo-3]: comparativa con otros gestores de procesos

Y no puede faltar, la documentación del proyecto: [docs][supervisor]

[supervisor]: http://supervisord.org/
[mongodb]: http://www.mongodb.org/
[supervisor-install]: http://supervisord.org/installing.html
[supervisor-examples]: http://supervisord.org/subprocess.html#examples-of-program-configurations
[articulo-1]: http://edvanbeinum.com/how-to-install-and-configure-supervisord
[articulo-2]: http://zerokspot.com/weblog/2012/06/17/sitemanagement-with-supervisord/
[articulo-3]: http://tech.cueup.com/blog/2013/03/08/running-daemons/