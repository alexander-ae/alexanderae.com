Title: Subir archivos a Amazon S3 directamente
Date: 2020-06-14
Tags: AWS,
Slug: subir-archivos-s3
Author: __alexander__
Summary: Como parte de un proyecto necesito que ciertos usuarios puedan cargar imágenes a Amazon S3. Esto puede realizarse sin necesidad de que el procesamiento se realice en un servidor que yo administre y es lo que se verá a continuación

Como parte de un proyecto necesito que ciertos usuarios puedan cargar imágenes a Amazon S3. Esto puede realizarse sin necesidad de que el procesamiento sea un servidor que yo administre, es decir, que el formulario puede configurarse para que envíe los archivos directamente a Amazon S3.

**Nota:** si bien es inseguro que permitamos que cualquier usuario suba archivos a nuestro servidor (no sabemos qué archivos subirá), en mi caso serán "usuarios de confianza".

- - -

Para lo anterior necesitamos realizar 2 tipos de tareas:

1. Crear y configurar los servicios necesarios en la consola de AWS
2. Escribir el código necesario para la carga de archivos

- - -

## Configuración de AWS

<br>
**1.1.-** Lo primero es crear un *bucket* en S3, así que nos dirigimos a la consola y escogemos la opción para crear un bucket.

![creación de un bucket en s3](/pictures/upload-s3/creacion-de-bucket.png)

<br>
**1.2.-** Permitimos el acceso público a nuestro bucket recién creado.
    
Para ello nos dirigimos a la configuración del bucket, sección "Permisos" - "Bloquear Acceso Público" y desmarcamos los checks.
 
<br>   
**1.3.-** Configuramos el CORS del bucket S3.
    
En la sección "Permisos" - "Configuración del CORS" añadimos un texto de la forma:

~~~
::xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>
~~~

Notando que el *"\*"* en *AllowedHeader* se refiere a que permitiremos que cualquier website solicite de nuestras imágenes. Esto tan solo lo realizaremos en nuestra demo ya que en realidad aquí debe ir el dominio que utilizaremos en nuestra web.

<br>
**1.4.-** Creamos un "conjunto de identidades anónimas" en "Amazon Cognito"

Para permitir que usuarios sin registrar puedan subir archivos, escogemos la opción de *"Administrar grupos de identidades"* y seleccionamos *"Crear nuevo grupo de identidades"*.

Note que marcaremos la opción de *"Habilitar acceso a indentidades sin autenticar"*

![creación de un grupo de identidades en aws cognito](/pictures/upload-s3/aws-cognito.png)

Copiamos el ID que nos entrega (lo usaremos más adelante)

![id secreto de aws cognito](/pictures/upload-s3/aws-cognito-secrets.png)

<br>
**1.5.-** Ahora debemos brindarles permisos al nuevo rol creado para que sea capaz de manipular archivos de S3.

En la consola de AWS, vamos al servicio "IAM", buscamos el rol creado, en mi caso algo similar a *Cognito_demo_1428Unauth_Role* y le asociamos una nueva política:

~~~
::json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket-1428/*"
            ]
        }
    ]
}
~~~

Y todo listo, al menos la primera parte que se refiere a la configuración de AWS.

<br>
## Código HTML / JS

Utilizaré *Cash.js*, una alternativa ligera a Jquery para algunas manipulaciones del DOM.

El html mínimo sería similar a:

~~~
::html
<form action=".">
    <label for="photo">
        Escoja la foto
        <input type="file" id="photo" name="file">
    </label>
</form>

<progress max=”100” value=”0”></progress>
~~~

Tenemos una barra de progreso de la carga, pero no es necesaria, se puede omitir.

Luego debemos incluir el javascript del SDK de AWS (ver referencias) y el código de cash.js (puede utilizarse jquery o vanilla js)

~~~
::html
<script src="https://cdnjs.cloudflare.com/ajax/libs/cash/7.0.3/cash.min.js"></script>
<script src="https://sdk.amazonaws.com/js/aws-sdk-2.696.0.min.js"></script>
~~~

Y la lógica principal:

~~~
::javascript
    var bucketName = 'demo-bucket-1428';
    var bucketRegion = 'us-east-1';
    var IdentityPoolId = "us-east-1:credenciales-super-secretas";

    AWS.config.update({
        region: bucketRegion,
        credentials: new AWS.CognitoIdentityCredentials({
            IdentityPoolId: IdentityPoolId
        })
    });

    var s3 = new AWS.S3({
        apiVersion: '2006-03-01',
        params: {Bucket: bucketName}
    });

    $('form').on('change', function (ev) {
        ev.preventDefault();
        $('body').css('cursor', 'progress');
        let files = document.getElementById('photo').files
        if (!files.length) return;
        saveFile(files);
    });

    function saveFile(files) {
        if (files) {
            let file = files[0];
            var fileName = file.name;
            var filePath = 'directorio_de_prueba/' + fileName;
            var fileUrl = 'https://s3.amazonaws.com/' + bucketName + '/' + filePath;

            s3.upload({
                Key: filePath,
                Body: file,
                ACL: 'public-read'
            }, function (err, data) {
                if (err) {
                    console.log(error)
                }
                $('body').css('cursor', 'default');
            }).on('httpUploadProgress', function (progress) {
                var uploaded = parseInt((progress.loaded * 100) / progress.total);
                $("progress").attr('value', uploaded);
            });
        }
    };
~~~

Y eso es todo, ahora tenemos nuestro formulario que sube archivos a S3 sin necesidad de que pase a través de nuestro servidor.

Como dato extra, para limitar los tipos de archivos permitidos, podemos seguir el siguiente post: <a href="https://aws.amazon.com/es/premiumsupport/knowledge-center/s3-allow-certain-file-types/" target="_blank">How can I allow only certain file types to be uploaded to my Amazon S3 bucket?</a>

## Referencias

* <a href="https://github.com/fabiospampinato/cash" target="_blank">Cash JS</a>: An absurdly small jQuery alternative for modern browsers.

* <a href="https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/s3-example-photo-album.html" target="_blank">Uploading Photos to Amazon S3 from a Browser</a>

* <a href="https://medium.com/@shresthshruti09/uploading-files-in-aws-s3-bucket-through-javascript-sdk-with-progress-bar-d2a4b3ee77b5" target="_blank">Uploading Files in AWS S3 Bucket through JavaScript SDK with Progress Bar</a>

* <a href="https://github.com/aws/aws-sdk-js" target="_blank">AWS SDK JS</a>
