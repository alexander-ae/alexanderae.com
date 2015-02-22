Title: RiotJS: Tutorial #1
Date: 2015-02-22
Tags: riotjs,javascript,parse,tutorial
Slug: riotjs-tutorial-1
Author: __alexander__

Ahora que cuento con un tanto de tiempo libre, es momento de revisar algunos frameworks javascript.

Después de analizar las opciones (y vaya que son muchas) comenzaré con RiotJS[^1].

[RiotJS][RiotJS] es un [framework javascript minimalista][riot-2.0], entre sus características destacadan: el sistema de etiquetas personalidadas, su sencilla sintaxis y su pequeño tamaño.

Nota: Este tutorial es una adaptación de "[The react tutorial for riot][react-tutorial-for-riot]", el cual a su vez es otra adaptación del tutorial de [ReactJS][ReactJS-tutorial] para  RiotJS.

- - -

El objetivo del tutorial[^2] es construir un sistema de comentarios que podría incluirse en un blog. Las características de este sistema son:

- Tiene una vista de todos los comentarios anteriores
- Cuenta con un formulario para registrar nuevos comentarios
- Se integra con un backend para almacenar los comentarios[^3]

Y como adicionales:

- Comentarios optimistas: los comentarios aparecen antes de ser registrados en el backend
- Actualizaciones en vivo, es posible ver los comentarios de otras personas en tiempo real.

- - -

#### 1. Estructura

Los bloques a considerar para nuestra implementación son:

    - CommentBox
        - CommentList
            - Comment
        - CommentForm

Los cuales se refieren al contenedor general, la lista de comentarios, cada comentario propiamente dicho y al formulario.

Como mencionamos, uno de los puntos fuertes de Riot es que nos permite usar etiquetas personalizadas. Para aprovechar esto crearemos un archivo llamado *comments.tag* y escribiremos lo siguiente en el:

~~~
::text
    <comment-box>
      <h1>Comentarios</h1>

      <comment-list comments={ comments } />
      <comment-form />
    </comment-box>

    <comment-form>
      <form>
        <input type="text" name="name">
        <textarea name="message"></textarea>
        <input type="submit" value="Publicar">
      </form>
    </comment-form>

    <comment-list>
      <comment each={ opts.comments } />
    </comment-list>

    <comment>
      <div>
        <h2>Mi nombre</h2>
        <p>Mi comentario</p>
      </div>
    </comment>
~~~

Lo anterior representa a los bloques inicialmente descritos:

- Nuestro `comment-box` que tiene un elemento `comment-list` al cual le está pasando como parámetro la lista de comentarios.
- El `comment-form` que representa al formulario por el que se registran nuevos comentarios
- El `comment-list` que contiene una lista de elementos `comment` sobre la que va a iterar.
- El `comment` que es el comentario propiamente dicho.

<br>

#### 2. Montar los componentes

Ahora que tenemos los componentes, vamos a integrarlos con nuestra web.

Nuestro archivo HTML principal (index.html) debe lucir similar a:

~~~
::html
<html>
    <head>
        <title>Sistema de comentarios</title>
        <script src="riot.min.js"></script>
    </head>

    <body>
        <comment-box></comment-box>

        <script src='comments.js'></script>

        <script>
            riot.mount('comment-box');
        </script>

    </body>
</html>
~~~

Nota: estoy usando riot.js desde la rama `dev`, aun no publicada a la fecha (por un bug relacionado al método `update`)

En el html, hemos incluido nuestro contentenedor general (`<comment-box>`), el archivo `comments.js` y un script que monta[^4] nuestra etiqueta `<comment-box>`.

Observen además que hemos incluido un script `comments.js` en el documento, este se obtiene al compilar nuestro archivo *comments.tag*.

<br>

Para compilar el archivo `.tag` tenemos dos opciones:

*1.* Incluir el archivo `compiler.js` en el head de nuestra página

*2.* Compilar en el lado del servidor, para ello necesitamos instalar riot mediante npm:

>    `npm install riot`

Con ello tendremos acceso al binario **riot**, al cual le indicaremos que observe los cambios en los archivos *tag* en nuestro directorio actual y los compile:

>   `riot -w .`

Para comprobar si todo va bien hasta ahora, podríamos levantar un servidor en local:

>    `python -m SimpleHTTPServer`

si vamos a `127.0.0.1:8000`, veremos que solo se ha cargado el formulario (nota: verificar que no exista ningún error en el inspector de elementos[^5])

En el siguiente paso añadiremos algunas funcionalidades.

<br>

#### 3. Incluyendo variables y estados

Otra de las características de riot nos permite enviar variables al tag[^6] que estamos montando.

Editamos el archivo `index.html`, cambiamos la línea que monta el tag por:

>   `riot.mount('comment-box', {title: 'Comentarios'});`

y actualizamos nuestro archivo `.tag` para que incluya nuestra variable `title`:

~~~
::text
<comment-box>
  <h1>{ opts.title }</h1>

  <comment-list comments={ comments } />
  <comment-form />
</comment-box>
~~~

&#42;Las opciones que enviamos a nuestro tag como contexto quedan almacenadas en la variable `opts`[^7], con lo que el título de nuestra tag será el parámetro que enviamos.

Añadiendo un poco más de código para manejar el registro de nuevos comentarios:

~~~
::text
<comment-box>
  <h1>{ opts.title }</h1>

  <comment-list comments={ comments } />
  <comment-form />

  this.comments = []
  add(comment) {
    this.comments.push(comment)
  }
</comment-box>

<comment-form>
  <form onsubmit={ add }>
    <input type="text" name="name">
    <textarea name="message"></textarea>
    <input type="submit" value="Publicar">
  </form>

  add(e) {
    var comment = {
      name: this.name.value,
      message: this.message.value
    }
    this.parent.add(comment)
    e.target.reset()
  }
</comment-form>

<comment-list>
  <comment each={ opts.comments }/>
</comment-list>

<comment>
  <div>
    <h2>{ this.parent.name }</h2>
    <p>{ this.parent.message }</p>
  </div>
</comment>
~~~

Hemos creado una función `add(e)` que maneja el evento *onsubmit* de nuestro formulario. Esta función captura los valores ingresados, los envía al tag padre (`<comment-box>`) y resetea[^8] el formulario. Observe que los campos con un atributo name se pueden acceder directamente mediante `this.name`


En el tag `<comment-box>` se tiene otra función que inserta el comentario en la lista de comentarios.

También, en nuestra etiqueta `comment` estamos mostrando los atributos `name` y `message` de cada iteración, por medio de los atributos del padre.

Otra opción más *"explícita"* sería enviando el nombre y mensaje como variables de contexto:

~~~
::text
<comment-list>
  <comment each={ opts.comments } name={ this.name } message={ this.message }/>
</comment-list>

<comment>
  <div>
    <h2>{ opts.name }</h2>
    <p>{ opts.message }</p>
  </div>
</comment>
~~~

Con lo realizado hasta ahora, podemos volver a abrir nuestro navegador y probar.

<br>

#### 4. Carga y persistencia de nuestros comentarios

Lo que sigue es implementar la comunicación de nuestra aplicación con algún backend para que los comentarios registrados queden almacenados. Para el ejemplo, voy a utilizar [Parse][ParseJS].

Nos registramos y creamos una [nueva aplicación][parse-apps]. Luego copiamos los valores del `Application ID` y el `Javascript Key`.

En nuestro archivo html debemos insertar el script de parse (para facilidad nuestra, podemos usar el del CDN):

> `<script src="//www.parsecdn.com/js/parse-1.3.4.min.js"></script>`

Luego, debemos inicializar la aplicación:

> `Parse.initialize("APP_KEY", "JS_KEY");`

En nuestra etiqueta `comment-box`, modificamos el método `add` para que también registre el comentario en Parse:

~~~
::javascript
add(comment) {
  this.comments.push(comment)
  var Comment = Parse.Object.extend("Comment")
  var _comment = new Comment()
  _comment.save(comment)
}
~~~

Añadimos también un método `load` que realizará la [carga][parse-load] de comentarios desde Parse:

~~~
::javascript
load() {
  var self = this
  var Comment = Parse.Object.extend('Comment')
  var queryComment = new Parse.Query(Comment)

  queryComment.find({
    success: function (results) {
      var tmp_comments = []
      for (var i = 0; i < results.length; i++) {
        tmp_comments.push(results[i].toJSON())
      }

      self.update({'comments': tmp_comments})
    },
    error: function (error) {
      alert("Error: " + error.code + " " + error.message)
    }
  })
}
~~~

Nótese que al terminar de recuperar los comentarios, estamos activando manualmente el evento update para que se refresquen los comentarios visibles.

También debemos iniciar nuestro método manualmente al menos una vez `this.load()`.

Luego, para que el sitio refresque los comentarios cada cierto tiempo, podemos añadir:

>   setInterval(this.load, opts.interval)

Y en nuestra llamada al `mount` en el index, agregamos el parámetro interval:

>   riot.mount('comment-box', {title: 'Comments', interval: 2500});

<br>

- - -

Pueden revisar la versión final del código en este [gist][gist-demo].

Como se observa en el resultado final, lo que me sorprende es la poca cantidad de código que se requiere para tener un sistema de comentarios con persistencia en el backend haciendo presente que tampoco se pierde legibilidad en el código.

- - -

Referencias:

- [The react tutorial for riot][react-tutorial-for-riot]


[^1]: El plan original incluye revisar AngularJS y ReactJS también.

[^2]: El detalle es casi idéntico al tutorial de ReactJS, tan solo difiere en la capacidad para realizar comentarios con markdown.

[^3]: Como backend estoy utilizando [ParseJS][ParseJS]

[^4]: RiotJS llama montar al proceso de incluir nuestras etiquetas personalizadas y su respectiva lógica en el documento HTML.

[^5]: Me refiero al inspector de elementos de chrome o a su equivalente en firefox.

[^6]: tag o etiqueta

[^7]: [riot.js mount][riot.js mount]

[^8]: Se puede acceder al elemento que origina el evento con `e.target`. Para más detalle, consultar la documentación: [https://muut.com/riotjs/guide/#event-object][riot.js event]

[react-tutorial-for-riot]: https://juriansluiman.nl/article/154/the-react-tutorial-for-riot
[ReactJS-tutorial]: http://facebook.github.io/react/docs/tutorial.html
[RiotJS]: https://muut.com/riotjs/
[riot-2.0]: https://muut.com/blog/technology/riot-2.0/index.html
[ParseJS]: https://www.parse.com
[parse-apps]: https://parse.com/apps
[parse-load]: https://parse.com/docs/js_guide#objects-retrieving
[gist-demo]: https://gist.github.com/alexander-ae/cff216db327e07c07bea
[riot.js mount]: https://muut.com/riotjs/api/#mount
[riot.js event]: [https://muut.com/riotjs/guide/#event-object]