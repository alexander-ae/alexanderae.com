Title: Programar backup de Mysql en Windows
Date: 2013-04-14 14:45
Tags: mysql, sysadmin, windows,
Slug: programar-backup-de-mysql-en-windows
Author: __alexander__

Tal y como mencioné en la entrada anterior, tuve que instalar django con **mysql** como base de datos en windows server. Además, se tuvo que usar un script para realizar copias automáticas de la base de datos.

#### Script

El script, el cual encontré [aquí][oscar.org] y modifiqué levemente fue:

    @echo off
    set mySqlPath=C:\wamp\bin\mysql\mysql5.5.x
    set dbUser=usuario_backup
    set dbPassword="mi_contraseña"
    set dbName=mi_base_de_datos
    set file=%dbName%_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.sql
    set path=C:\%dbName%

    echo Running dump for database %dbName% ^> ^%path%\%file%
    "%mySqlPath%\bin\mysqldump.exe" -u %dbUser% -p%dbPassword%  %dbName% >"%path%\%file%"
    echo Done!

Note que podemos configurar el formato del nombre de salida del archivo (set file) o la ubicación de las copias (set path) a nuestro gusto.


#### Programando la tarea

Windows cuenta con la utilidad llamada "[at][at]" (Task scheduler o Programador de tareas) que será la que se usará:

Podemos listar las tareas con el comando: "at" e insertar la la tarea del siguiente modo:

    at 23:30 /every:M,T,W,Th,F,S,Su C:\backup\scripts\mysql-backup.bat

Con lo que lograremos que nuestro script se ejecute todos los días a las 23:30.


[oscar.org]: http://www.oskar.org/blog/2012/jan/scheduled-backup-of-mysql-databases-in-windows
[at]: http://en.wikipedia.org/wiki/At_(Windows)