Title: Jquery StickyBox
Date: 2013-02-17
Tags: jquery, js
Slug: jquery-stickybox
Author: __alexander__

Plugin para jquery que genera bloques flotantes siguen al usuario cuando se desplaza la página. Utiliza posicionamiento absoluto en base a los estilos css iniciales.

 Por ejemplo, se podría usar en los siguientes casos:

- Para realizar carritos de compras que muestran información de la compra actual
- En caso de querer añadir botones sociales (facebook, twitter..)
- Para generar menús flotantes

#### Requerimientos e Instalación
El plugin requiere tanto de [jquery][jquery] como de [jquery easing][jquery-easing].

Los scripts **js** requeridos son:

        <script src="http://code.jquery.com/jquery-1.8.3.min.js"></script>
        <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery-easing/1.3/jquery.easing.min.js'></script>
        <script src='js/stickysidebar.jquery.min.js'></script>

Por ejemplo, el código **html** para un carrito de compras flotante podría ser:

        <aside id="sidebar">
          <div id="basket">
            <h3>Carrito de compras</h3>
            <p id="items" class='zero-items'>0</p>
          </div>
        </aside>

E inicializaríamos el plugin mediante:

~~~
::jquery
$("#sidebar").stickySidebar({
    timer: 200,
    easing: "easeInOutQuad",
    padding: 50
});
~~~

En su [sitio web][sticky-sidebar-jquery-plugin] podremos ver con un poco de más de detalle los parámetros disponibles y un par de ejemplos del mismo.

A modo de práctica yo repliqué el primero de sus ejemplos (carrito de compras) con algunos detalles adicionales, el cual puede verse [aquí][demo].

![demo-img][demo-img]

Código en github del plugin: [sticky-sidebar-jquery-plugin][repo-plugin]

Código en bitbucket de la demo que realizé: [demo][repo-demo] (el directorio es: sticky-sidebar-jquery-plugin)



[jquery]: http://jquery.com/
[jquery-easing]: http://gsgd.co.uk/sandbox/jquery/easing/
[sticky-sidebar-jquery-plugin]: http://www.profilepicture.co.uk/sticky-sidebar-jquery-plugin/
[demo]: http://labs.alexanderae.com/html-js-css/sticky-sidebar-jquery-plugin/
[repo-plugin]: https://github.com/p-m-p/jQuery-Stickybox
[repo-demo]: https://bitbucket.org/__alexander__/alexander-ae-site-static-demos

[demo-img]: /static/pictures/sticky-sidebar-jquery-plugin.png 'Captura de pantalla'