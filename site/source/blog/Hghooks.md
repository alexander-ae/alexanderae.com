Title: hghooks
Date: 2013-05-19 19:00
Tags: python, mercurial,
Slug: hghooks
Author: __alexander__

##### ¿Qué es un hook? #####

En [mercurial][mercurial], al parecer también en git, y tal vez en algún otro scv[^1] se le denomina hook a una acción programada para lanzarse al ocurrir algún evento en nuestro repositorio. Por ejemplo en *mercurial* podemos controlar los eventos:

- commit: después de terminar un commit
- precommit: antes de iniciar un commit
- update: después de que un update o merge halla finalizado en el repositorio local.

entre otros ..

##### hghooks #####

hghooks es un conjunto de hooks para usar con *mercurial*. Nos ofrece de los siguientes módulos:

- validación de código python por medio de [pep8][pep8]
- validación de código python por medio de pyflakes
- checkeo de sentencias pdm en python
- integración con track

En mi caso, lo utilizo para validar código python según estilos pep8 antes de realizar un commit.

##### Instalación y Uso: #####

1. Instalamos pep8 y hghook

        sudo easy_install pep8 hghooks

2. En el archivo .hg/hgrc de nuestro repositorio en el que activaremos el hook, añadimos:

        [hooks]
        pretxncommit.pep8 = python:hghooks.code.pep8hook

3. Listo, ahora cada vez que intentemos realizar un commit, se validará si antes nuestro código cumple con los estilos pep8

*Nota:*

Para ignorar alguna regla de pep8, agregamos unas lineas como la siguientes a nuestro archivo [hgrc][hgrc]:

        [pep8]
        ignore = E501 E128

*Referencias:*

↳ Mercurial: The Definitive Guide: [Chapter 10 Handling repository events with hooks][mercurial-tdg]

↳ [hghooks][hghooks]


[^1]: Sistema de control de versiones

[mercurial]: http://mercurial.selenic.com/
[hgrc]: http://www.selenic.com/mercurial/hgrc.5.html
[mercurial-tdg]: http://hgbook.red-bean.com/read/handling-repository-events-with-hooks.html
[hghooks]: https://pypi.python.org/pypi/hghooks/
[pep8]: http://www.python.org/dev/peps/pep-0008/