Title: Django Apps: South
Date: 2013-01-25 18:50
Tags: django, django-apps, base-de-datos
Slug: django-apps-south
Author: __alexander__

Se me ha dado por iniciar una revisión de algunas de las aplicaciones que uso en conjunto con [django][django], lo que me permitirá de algún modo no solo el transmitir conocimiento, sino también afianzar lo que sé, ya que para redactar los artículos deberé de leer un tanto de la documentación (a modo de repaso).

Iniciaré con [south][south], una aplicación que nos permite realizar migraciones de datos en nuestros proyectos/aplicaciones.

#### ¿Qué es una migración?

Se refiere al cambio del esquema de la base de datos de una versión a otra. Por ejemplos:

- El añadir un nuevo modelo(tabla) a nuestra aplicación.
- El añadir o remover un campo de nuestro modelo.
- El cambiar uno de los atributos de alguna tabla por ejemplo de null=False a null=True
- Como nos indican en la documentación, para south una migración incluye el crear el esquema inicial de nuestra base de datos.

#### ¿Por qué debo usar south?

- south puede leer automáticamente los cambios que hemos realizado en nuestra base de datos y crear con un simple comando ingresado la migración necesaria. (en caso de conflictos, requerirá intervención del usuario por medio de algún mensaje)

- Al igual que el ORM  de **Django**, es independiente del motor de base de datos a usar, esto quiere decir que no obtendremos problemas si usamos sqlite, mysql o postgresql. A la fecha[^database-api], el soporte para Microsoft SQL Server y Oracle estan en fase beta y alfa respectivamente.

- Permite manejar cada aplicación de manera independiente, es decir, podemos escoger que aplicaciones serán manejadas por south y cuales lo serán por medio del ya conocido 'syncdb'.

- South esta diseñado para detectar y advertirnos sobre conflictos introducidos por algún colaborador del proyecto mediante el sistema de control de versiones.


#### Instalación

Existen muchas maneras de instalar south, por medio de easy_install, pip, [clonando][south-mercurial] la última versión del repositorio en mercurial, alguno de los [paquetes descargables][south-packages] que nos otorgan o tal vez mediante el gestor de paquetes de nuestra distribución linux preferida (en el caso de que se incluyese south allí).

Mi método preferido[^south-install] es por medio de [pip][pip] ya que lo uso en conjunto con los entornos virtuales de [virtualenv][virtualenv]. Entonces por medio de pip, lo instalamos por medio de la siguiente instrucción:

~~~
pip install south
~~~

Y para nuestro proyecto en django añadimos **'south',** a la relación de aplicaciones instaladas (INSTALLED_APPS).

#### Tutorial

En la documentación de south podemos encontrar un [tutorial][south-tutorial] muy detallado sobre el uso de south, a continuación, un muy breve resumen:

##### Un nuevo proyecto en django con south

Por ejemplo, supongamos que estamos desarrollando un nuevo proyecto al que llamaremos ingeniosamente southTest con la aplicación testapp, la cual está enfocada a la administración de libros de una biblioteca.
    
Uno de los modelos de nuestra aplicación es el modelo libro, que contiene el título y el autor ambos como campos de texto.

- Lo primero a realizar es crear la primera migración de nuestra aplicación, lo cual podemos realizar con el comando
        
        ./manage.py schemamigration testapp --initial

- Con esto se debe de haber creado un directorio en nuestra aplicación conteniendo la migración inicial, tal y como se muestra en la siguiente imagen:

![proyecto: estructura][proyecto-estructura-01]

Antes de realizar la migración debemos de sincronizar la base de datos. Debido a que existe una migración para la aplicación 'testapp', el comando *syncdb* creará solo las tablas que están fuera de nuestra aplicación y nos indicará también cuales son las aplicaciones que estan o no administradas por south.

![proyecto-syncdb][proyecto-syncdb-01]

y tal como nos indica. ejecutamos la orden:

        ./manage.py migrate

con lo que se crea la única tabla de nuestro aplicación, la cual podemos observar desde el admin de django (en caso de haber registrado nuestro modelo)

![admin: Libro][admin-libro-01]

- Después de ingresar algunos libros, nos piden que la aplicación también deba de ser capaz de registrar los capítulos por cada libro, por lo que añadimos el modelo correspondiente:

![proyecto-models][proyecto-models]

creamos la migración con una variación del comando que usamos por primera vez y ejecutamos la migración:

        ./manage.py schemamigration testapp --auto
        ./manage.py migrate

a partir de este momento, cada nuevo cambio en el esquema de nuestra aplicación requerirá generalmente la ejecución de los dos comandos anteriores.

Con esto doy por terminado[^repo] este exageradamente pequeño tutorial, que lo que pretende es mostrar el uso de los comandos básicos de south, y que generalmente son los únicos que usaremos (espero realizar en algún momento una segunda parte con un uso más complejo de south).



[^database-api]: [South Database API][database-api]
[^south-install]: pip junto a easy_install son los métodos recomendados de instalación.
[^repo]: [Repositorio][repo] en bitbucket del proyecto de ejemplo

[django]: https://www.djangoproject.com/
[south]: http://south.aeracode.org/
[database-api]: http://south.readthedocs.org/en/latest/databaseapi.html#database-specific-issues
[south-mercurial]: http://south.readthedocs.org/en/0.7.6/installation.html#using-mercurial
[south-packages]: http://south.readthedocs.org/en/0.7.6/installation.html#using-downloadable-archives
[virtualenv]: http://www.virtualenv.org/en/latest/
[pip]: http://www.pip-installer.org/en/latest/
[south-tutorial]: http://south.readthedocs.org/en/latest/tutorial/index.html#tutorial
[repo]: https://bitbucket.org/__alexander__/test-django-south

[proyecto-estructura-01]: /static/pictures/django-south-02.png 'Estructura del proyecto'
[proyecto-syncdb-01]: /static/pictures/django-south-03.png 'syncdb'
[admin-libro-01]: /static/pictures/django-south-01.png 'admin: libro'
[proyecto-models]: /static/pictures/django-south-04.png 'models.py'