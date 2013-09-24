Title: Owncloud en webfaction
Date: 2013-09-21 11:00
Tags: owncloud, webfaction
Slug: owncloud-en-webfaction
Author: __alexander__

Después de probar owncloud en mi pc, en la cual utilizo [chakra linux][chakra-linux], intenté subirlo a webfaction, en donde tuve un pequeño problema.

Los pasos que seguí para instalar owncloud en webfaction (incluida la solución a mi problema) fueron:

1. En el panel de webfaction:

    1. Registramos un nuevo dominio: owncloud.midominio.com

    2. Registramos una nueva aplicación del tipo: **Static/CGI/PHP-5.x**

    3. Registramos un nuevo website en el que linkeamos el dominio y la aplicación.

    4. Creamos una nueva base de datos con su respectivo usuario (solo lo he probado con MySQL)

2. Accedemos por ssh al servidor:

    1. Descargamos owncloud:

        wget http://download.owncloud.org/community/owncloud-5.0.x.tar.bz2

    2. Extraemos los archivos al directorio de nuestra aplicación: *~/webapps/owncloud*

    3. Cambiamos los permisos[^1] de algunos directorios y archivos:

~~~
# permisos de directorios
find ~/webapps/owncloud -type d | xargs setfacl -m u:apache:r-x
find ~/webapps/owncloud -type d | xargs setfacl -m u:nginx:r-x

# permisos de archivos
find ~/webapps/owncloud -type f | xargs setfacl -m u:apache:r--
find ~/webapps/owncloud -type f | xargs setfacl -m u:nginx:r--
~~~

---

Hasta este punto, ya somos capaces de acceder por medio del navegador a la url de nuestra aplicación y comenzar a realizar la configuración (primer usuario, conexión a la base de datos..)

Pero si intentamos loguearnos desde algún cliente de escritorio o en mi caso, con la aplicación en android, obtendremos un error de credenciales.

Por suerte (para mí), este error ya le había sucedido a otra persona[^2], la cual publicó su caso. Al parecer **owncloud** utiliza mod_rewrite (un módulo de apache) para obtener el usuario y el password de las cabeceras HTTP cuando nos logueamos. Y en webfaction, este mecanismo esta desactivado.

Entonces, lo que hay que hacer es:

1. Añadir al archivo .htacces de *owncloud* una regla que redireccione la url inicial a una que contenga los parámetros de login y remover el header de Autorización que ya no usaremos:

        RewriteCond %{HTTP:Authorization} ^Basic.*
        RewriteRule ^(.*) $1?Authorization=%{HTTP:Authorization} [QSA,C]
        RequestHeader unset Authorization

2. Luego, para que *owncloud* sepa que hacer con estos nuevos parámetros, hay que editar el archivo *~/webapps/owncloud/lib/base.php*, y en la función init() añadir:

~~~
::php

//sett http auth headers for Webfaction workaround
if(isset($_GET['Authorization']) && preg_match('/Basic\s+(.*)$/i', $_GET['Authorization'], $matches))
{
    list($name, $password) = explode(':', base64_decode($matches[1]));
    $_SERVER['PHP_AUTH_USER'] = strip_tags($name);
    $_SERVER['PHP_AUTH_PW'] = strip_tags($password);
}
~~~

Y con ello ya estaría todo listo!

---

*Actualización: 23/09/2013*

Owncloud necesita ejecutar tareas de fondo periódicamente (como buscar nuevas noticias si se usa la aplicación *news*), para lo cual se cuenta con [3 opciones][background-jobs]: Ajax, webcron y cron.

En mi caso, utilizo cron, el cual para usarse en webfaction necesita que editemos el archivo de cron con el comando **crontab -e**.

Y añadiendo una entrada del tipo:

        */20  *  *  *  * /usr/local/bin/php54 -f ~/webapps/owncloud/cron.php > $HOME/cron.log 2>&1

con lo que ejecutaremos el cron.php cada 20 minutos y mantendremos un archivo log llamado cron.log.

Nota: es posible que prefiramos usar algun otro editor al que se usa por defecto para manipular el archivo cron. Lo podemos cambiar ajustando la variable *EDITOR*, por ejemplo: **export EDITOR=nano**


[^1]: Visto en los [foros de webfaction][setup-owncloud]
[^2]: Matthias Blaicher publicó la solución en su [blog][blaicher.com].

[chakra-linux]: http://www.chakra-project.org/
[setup-owncloud]: http://community.webfaction.com/questions/13195/setup-owncloud
[blaicher.com]: http://www.blaicher.com/2012/07/fixing-authentication-of-owncloud-for-webfaction/
[background-jobs]: http://doc.owncloud.org/server/5.0/admin_manual/configuration/background_jobs.html