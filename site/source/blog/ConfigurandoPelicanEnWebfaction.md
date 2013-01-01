Title: Configurando Pelican en webfaction
Date: 2012-12-25 15:38
Tags: pelican, webfaction, back-end
Slug: configurando-pelican-en-webfaction
Author: __alexander__

Ya que este sitio se encuentra alojado en webfaction y es generado gracias a [Pelican][pelican], me pareció que debía de realizar una breve explicación de los pasos que seguí para configurarlo.

Por la naturaleza del contenido, la aplicación que necesitamos crear debe ser del tipo estática. En webfaction podemos crear aplicaciones estáticas, entre las que tenemos 2 clases principalmente:

1. Static/CGI/PHP: permiten interpretar scripts CGI y aplicaciones PHP.
2. Static only: sirve exclusivamente archivos estáticos lo que se traduce en un menor consumo de memoria[^webfaction-static].

Para nuestro caso, nos bastará con la del tipo *static only*

![webfaction static image][webfaction-static-image]

Una vez creada la aplicación, debemos de configurar nuestro sitio para generar los archivos respectivos en el directorio asignado, el cual estará ubicado por ejemplo en: *$HOME/webapps/static_app*

**Pelican** maneja los parámetros de *producción* de nuestro proyecto en el archivo llamado 'publishconf.py'. Para lo anterior, debemos de incluir la siguiente linea:

    OUTPUT_PATH = '/home/<nombre_de_usuario>/webapps/static_app'

donde static_app corresponde a nuestra aplicación estática creada.

despues de configurar nuestra aplicación[^virtualenv] podemos ejecutar el comando:

    make publish

que colectará los archivos generados en el directorio indicado.

Aunque muy posiblemente exista alguna otra mejor manera, de momento es la que uso; y por lo que veo, a diferencia de configurar algún otro tipo de aplicación[^django] en webfaction, configurar pelican resulta exageradamente sencillo.

Ahora lo que sigue, al menos para mí, será el aprender a usar [fabric][fabric] para automatizar la tarea de publicar entradas.


[^webfaction-static]: <http://docs.webfaction.com/software/static.html>

[^django]: como django, que incluye creación de una base de datos, de la aplicación django propiamente dicha y la que maneja los *static* y *media*.

[^virtualenv]: he asumido que se tiene un entorno (posiblemente con virtualenv) en el que hemos instalado la pelican y los requerimientos adicionales de nuestra aplicación.

[pelican]: http://docs.getpelican.com/en/latest/ 'pelican static site generator'

[webfaction-static-image]: /static/pictures/webfaction-new-app-static.png 'webfaction new static app'

[fabric]: http://docs.fabfile.org/en/1.5/
