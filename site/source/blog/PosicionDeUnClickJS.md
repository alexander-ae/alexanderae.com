Title: Posición absoluta y Relativa de un click en javascript
Date: 2013-02-24
Tags: jquery, js
Slug: posicion-de-click-en-js
Author: __alexander__

Mientras intentaba desarrollar un plugin para jquery tuve un inconveniente, el cómo hacer para obtener la posición relativa de un evento click hacia su contenedor.

Realizando algunas búsquedas en google y leyendo los diversos artículos pude obtener una idea del cómo estaba el panorama. Por ejemplo, revisando el tutorial de **jquery** que versa sobre el [cálculo de la posición del mouse][jquery-mouse-position] podemos destacar algunos puntos:

- *pageX*[^pageX] y *pageY* son dos propiedades de todos los eventos javascript que nos indican la posición absoluta del puntero respecto a la esquina izquierda de todo documento (no solo de la parte visible de la página).

- Para realizar el cálculo de la posición relativa de un click nos muestran el siguiente ejemplo:

~~~
::jquery
$("#special").click(function(e){

    var x = e.pageX - this.offsetLeft;
    var y = e.pageY - this.offsetTop;

    $('#status2').html(x +', '+ y);
});
~~~

lo que consiste en el cálculo de la posición absoluta del click menos la posición absoluta del contenedor.


#### stackoverflow

En mi búsqueda del como poder realizar esto, di con algunos enfoques interesantes en [stackoverflow][stackoverflow]:

Por ejemplo, había quien recomendaba realizar un cálculo iterativo de las distancias relativas de cada contenedor con su padre:

~~~
::jquery
function absolutePos(obj) {
    var curleft = curtop = 0;
    if (obj.offsetParent) {
        do {
            curleft += obj.offsetLeft;
            curtop += obj.offsetTop;
        } while (obj = obj.offsetParent);
    }
    return [curleft,curtop];
}
~~~

Note que *offsetLeft*[^offsetLeft] calcula la distancia del elemento actual en relación a su contenedor o padre.

Y también quien sugería una [mejora][calculo-iterativo] introduciendo los valores del *margin*, *padding* y *border*:

~~~
::javascript
function getNumericStyleProperty(style, prop){
  return parseInt(style.getPropertyValue(prop),10) ;
}

function element_position(e) {
    var x = 0, y = 0;
    var inner = true ;
    do {
        x += e.offsetLeft;
        y += e.offsetTop;
        var style = getComputedStyle(e,null) ;
        var borderTop = getNumericStyleProperty(style,"border-top-width") ;
        var borderLeft = getNumericStyleProperty(style,"border-left-width") ;
        y += borderTop ;
        x += borderLeft ;
        if (inner){
            var paddingTop = getNumericStyleProperty(style,"padding-top") ;
            var paddingLeft = getNumericStyleProperty(style,"padding-left") ;
            y += paddingTop ;
            x += paddingLeft ;

            var marginTop = getNumericStyleProperty(style,"margin-top") ;
            var marginLeft = getNumericStyleProperty(style,"margin-left") ;
            y += marginTop ;
            x += marginLeft ;
        }
        inner = false ;
    } while (e = e.offsetParent);
    return { x: x, y: y };
}
~~~

Y por último, la solución a mi problema. Al parecer existen un par de propiedades de los eventos que indican la posición relativa al contenedor en el que fueron realizados: **offsetX**[^offsetX] y offsetY.
Por lo que para nuestros propósitos, bastaría con algo como:

~~~
::jquery
$('selector').click(function(ev){
    x = ev.offsetX;
    y = ev.offsetY;
}
~~~

y todo parecería perfecto .. exceptuando por un *'insignificante'* problema, **offsetX** no está definido[^offsetX-firefox] en Firefox.
Pero menos mal que si revisamos en [stackoverflow][offsetX-firefox-stackoverflow] nuevamente, podremos encontrar alguna solución, como por ejemplo:

~~~
::jquery
if(ev.offsetX == undefined){ // para firefox
    x = ev.pageX - $(this).offset().left;
    y = ev.pageY - $(this).offset().top;
}
else{ // chrome
    x = ev.offsetX;
    y = ev.offsetY;
}
~~~

#### demo
A modo de [ejemplo][demo], armé una [demo][demo] en la que se trata de dibujar un punto de 2x2 en la posición en la que se realiza un click tal y como muestra la siguiente captura:

![demo][demo-img]

*Notas:*

- En el ejemplo se comparan el método encontrado en la documentación de jquery así como la solución que utilicé, imprimiendo ambos resultados en la consola.
- Observando que si bien en chrome ambos cálculos coinciden, en firefox hay una diferencia de 4px posiblemente al margin que le di al body (requeriría un mayor análisis).
- Para dibujar el punto solo se utilizó la solución que expuse como final.

![consola del firebug en firefox][demo-img-firefox]

Código en bitbucket del ejemplo: [demo][repo-demo] (el directorio es: posicion-relativa-de-un-click)

[^pageX]: Mozilla developers: [pageX][pageX]
[^offsetLeft]: Mozilla developers: [offsetLeft][offsetLeft]
[^offsetX]: Especificación de la propiedad: [offsetX][offsetX]
[^offsetX-firefox]: [reporte][offsetX-firefox] del bug en bugzilla

[jquery-mouse-position]: http://docs.jquery.com/Tutorials:Mouse_Position
[stackoverflow]: http://stackoverflow.com/
[pageX]: https://developer.mozilla.org/en-US/docs/DOM/event.pageX

[calculo-iterativo]: http://stackoverflow.com/a/5776220/1472750
[offsetLeft]: https://developer.mozilla.org/en-US/docs/DOM/element.offsetLeft
[offsetX]: http://www.w3.org/TR/cssom-view/#dom-mouseevent-offsetx
[offsetX-firefox]: https://bugzilla.mozilla.org/show_bug.cgi?id=69787
[offsetX-firefox-stackoverflow]: http://stackoverflow.com/q/12704686/1472750
[repo-demo]: https://bitbucket.org/__alexander__/alexander-ae-site-static-demos
[demo]: http://labs.alexanderae.com/posicion-relativa-de-un-click/

[demo-img]: /pictures/posicion-de-un-click-demo.png 'Demo'
[demo-img-firefox]: /pictures/posicion-de-un-click-demo-firefox.png 'Consola en firefox'