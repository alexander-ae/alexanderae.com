Title: Autodeploy en Gitlab
Date: 2017-07-09
Tags: git,sysadmin,
Slug: autodeploy-en-gitlab
Author: __alexander__

En la industria del software siempre se busca automatizar las tareas repetitivas para dedicarle más tiempo a las que son realmente importantes. Una de estas tareas repetitivas es el llamado **deploy**.

El *deploy*[^1] consiste en el conjunto de actividades que realizamos para que el software sea usable por el público.

- - -

Como ejemplo, listo las tareas que realizo para actualizar un proyecto que tiene html's estáticos:

1. Publicamos de un nuevo cambio en el repositorio, gitlab para nuestro caso (push)
2. Nos conectamos al servidor
3. Actualizamos el código en el servidor (pull)
4. Copiamos los archivos del proyecto al directorio en que el servidor web (nginx) trabaja.
5. Visualizamos los cambios en el website mediante el navegador


- - -

## ¿Cómo reducir el trabajo manual?

Encontré una aplicación opensource llamada [Git-Auto-Deploy][Git-Auto-Deploy] que actua como un pequeño servidor cuya función es escuchar los webhooks[^2] que se lanzan cada vez que publicamos un cambio en el repositorio.

Los pasos a seguir para tenerlo configurado en nuestro servidor son:

*1.* Crear una llave ssh pública en el servidor: `ssh-keygen -t rsa ` y luego la copiamos `cat ~/.ssh/id_rsa.pub`

*2.* Agregamos la clave como *deployment key* en el panel del repositorio de gitlab:

![gitlab deployment][gitlab-deployment]

*3.* En el servidor en el que se va a realizar el auto-deploy clonamos la aplicación: `git clone https://github.com/olipo186/Git-Auto-Deploy.git`

*4.* En el directorio de *Git-Auto-Deploy*, duplicamos el archivo de configuración de ejemplo: `cd GitDeploy; cp config.json.sample config.json`

*5.* Editamos el archivo de configuración, el mio quedó similar a:

~~~
{
  "http-port": 8002,
  "log-file": "~/gitautodeploy.log",
  "pid-file": "~/.gitautodeploy.pid",
  "log-level": "INFO",

  "repositories": [
    {
      "url": "git@gitlab.com:test/test.git",
      "branch": "master",
      "remote": "origin",
      "path": "/var/www/test/",
      "deploy": "echo deploying;cp -r /var/www/test/* /var/www/html/.;echo end",
      "secret-token": "my-secret-gitlab-token"
    }
  ]
}
~~~

*6.* Ejecutamos la aplicación en segundo plano: `python2.7 GitAutoDeploy.py -d`

*7.* Registramos el webhook en gitlab: Gitlab: Settings : Integrations

![gitlab webhooks][gitlab-webhooks]

*8.* Esto es todo, ahora cada que realicemos un push, la secuencia de comandos que hayamos registrado se debe ejecutar.

## Referencia:

- Autodeploy your gitlab projects: [autodeploy-gitlab-post]

[gitlab-deployment]: /pictures/gitlab-deployment-key.png 'gitlab deployment keys'
[gitlab-webhooks]: /pictures/gitlab-webhooks.png 'gitlab webhooks'

[Git-Auto-Deploy]: https://github.com/olipo186/Git-Auto-Deploy
[autodeploy-gitlab-post]: https://johnflynn.me/autodeploy-your-gitlab-projects/

[^1]: Sofware deployment: [https://en.wikipedia.org/wiki/Software_deployment][https://en.wikipedia.org/wiki/Software_deployment]
[^2]: Webhooks: [https://es.wikipedia.org/wiki/Webhook][https://es.wikipedia.org/wiki/Webhook]
