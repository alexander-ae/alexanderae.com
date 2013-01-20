Title: Resetear password de PostgreSQL
Date: 2013-01-12 10:27
Tags: postgresql, base-de-datos
Slug: recuperar-password-de-postgresql
Author: __alexander__

Recurrentemente he necesitado cambiar la contraseña del usuario '*postgres*' del postgresql, por lo cual incluyo aquí una nota[^1] para mi mismo y para a quien esto le pueda ayudar:

Pasos:

1. Abrimos una terminal y accedemos como usuario postgres:

        sudo su postgres

2. Ejecutamos [psql][psql] para acceder a la terminal interactiva de postgresql:

        psql

3. Ahora escribimos esta sentencia SQL que nos permitirá asignar una nueva contraseña al usuario postgres:

    alter user postgres with password 'nueva_contraseña';

4. Salimos de psql con:

        \q

5. Cerramos nuestra sesión como postgres:

        exit

y listo, contraseña cambiada.


[^1]: Visto en el blog de [Johan Hernandez][referencia]

[psql]: http://www.postgresql.org/docs/9.2/static/app-psql.html
[referencia]: http://johansoft.blogspot.com/2007/09/cambiar-contrasea-de-usuario-postgres.html
