Title: Jcanvas
Date: 2013-05-02 09:10
Tags: front-end, html, js, jquery, canvas
Slug: jcanvas
Author: __alexander__

[Jcanvas][jcanvas] es un plugin para jquery que nos permite interactuar con el [canvas][canvas] de html5.

Entre sus características principales, resaltan:

- API Sencilla que permite el manejo de figuras geométricas, imágenes, máscaras, capas, animaciones..
- Funciona en navegadores móbiles y de escritorio (aunque no lo he probado en ningún móbil)
- Ligero (~25kB)
- OpenSource

#### Instalación

Se requiere añadir tanto jquery como el propio plugin:

        <script src="jquery.min.js"></script>
        <script src="jcanvas.min.js"></script>

#### Uso

Se pueden observar 3 ejemplos sencillos [aquí][labs].

- - -

*1.* El primer ejemplo nos muestra el como añadir algunas figuras geométricas:

![demo-01][demo-01]

**HTML**

~~~~
::html
<canvas id="canvas1" width='480' height='320'></canvas>
~~~~

**JS**

Primero asignamos el canvas a una variable. Luego, podemos invocar a los métodos requeridos para dibujar figuras geométricas, como *drawArc* para arcos indicando las propiedades deseadas mediante un objeto en [json][json]. Es posible incluso concatenar los métodos.

~~~~
::jquery
var $canvas1 = $("#canvas1");

$canvas1.drawArc({
  fillStyle: "rgba(12,12,59,0.6)",
  x: 280, y: 80,
  radius: 25
});

$canvas1.drawArc({
  fillStyle: "black",
  x: 20, y: 72,
  radius: 10
}).drawArc({
  fillStyle: "#285714",
  x: 56, y: 48,
  radius: 18,
  start: 30, end: 280
});
~~~~

Podemos también, graficar elipses y rectángulos; asi como superponerlos, usar rgba, entre otros.

~~~~
::jquery
$canvas1.drawEllipse({
  fillStyle: "rgba(108, 96, 256, 0.5)",
  x: 250, y: 190,
  width: 40, height: 90,
  strokeWidth: 2
}).drawEllipse({
  fillStyle: "rgba(36, 144, 54, 0.5)",
  x: 250, y: 190,
  width: 90, height: 40,
  strokeWidth: 2
});

$canvas1.drawRect({
  fillStyle: "#d5d",
  x: 50, y: 50,
  width: 60,
  height: 30,
  fromCenter: false
});
~~~~

- - -

*2.* En el segundo ejemplo podemos observar el manejo de capas o grupos de las mismas:

![demo-02][demo-02]

*JS*

Considerando, el alto y ancho del canvas asi como el tamaño de la cuadrícula, la graficamos mediante rectas, las cuales guardamos como capas bajo el mismo grupo.

~~~~
::jquery
/* canvas 2 */
var $canvas2 = $("#canvas2");
var h = $canvas2.height();
var w = $canvas2.width();
var grid = 50;

// cuadricula
for (var i = 0; i<h; i=i+grid) {
  $canvas2.drawLine({
    layer: true,
    group: 'cuadricula',
    strokeStyle: "#000",
    strokeWidth: 1,
    x1: 0, y1: i,
    x2: w, y2: i
  });
}

for (i = 0; i<w; i=i+grid) {
  $canvas2.drawLine({
    layer: true,
    group: 'cuadricula',
    strokeStyle: "#000",
    strokeWidth: 1,
    x1: i, y1: 0,
    x2: i, y2: h
  });
}
~~~~

Por medio de un botón, mostramos u ocultamos el grupo de capas.

~~~~
::jquery
// mostrar/ocultar
var $show_hide_grid = $('#show_hide_grid');
var grid_visible = true;

$show_hide_grid.click(function() {
  if (grid_visible) {
    $show_hide_grid.text('Mostrar cuadricula');
    $canvas2.setLayerGroup("cuadricula", {
      visible: false
    }).drawLayers();
    grid_visible = false;
  }
  else{
   $show_hide_grid.text('Ocultar cuadricula');
    $canvas2.setLayerGroup("cuadricula", {
      visible: true
    }).drawLayers();
    grid_visible = true;
  }
});
~~~~

- - -

*3.* El tercer ejemplo muestra una esfera rebotando en el 'piso' por medio de una sencilla animación.

![demo-03][demo-03]

*JS*

Creamos la esfera:

~~~~
::jquery
var $canvas3 = $("#canvas3");

$canvas3.drawArc({
  layer: true,
  name: 'esfera',
  fillStyle: '#797',
  x: 240, y: 20,
  radius: 10
});
~~~~

Creamos la animación^1 y la iniciamos. Notar que hemos concatenado 2 animaciones, una para la caida al finalizar se ejecuta la subida. La función es recursiva, por lo que nunca termina.

~~~~
::jquery
var rebote = function(){
  $canvas3.animateLayer('esfera',
    {x: 240, y:310},
    2000, 'easeInQuad',
    function() {
      $(this).animateLayer("esfera", {
        x: 240, y: 20
      }, 2000, "easeOutQuad", rebote);
    }
  );
  return;
};

/* inicializa */
rebote();
~~~~

- - -

#### Notas adicionales

Para mayor información se puede visitar la [documentación][docs] del plugin. Del mismo modo, en su página se cuenta con un [sandbox][sandbox] para *probar sin romper nada*.

- Página del proyecto en [github][github].
- [Sitio][labs] de las demos mostradas


[^1]: Para el efecto de caida y subida se uso el plugin jquery: [easing][easing] . Usando como referencia [esta guía][easing-referencia] para saber que función usar.

[jcanvas]: http://calebevans.me/projects/jcanvas/
[canvas]: http://es.wikipedia.org/wiki/Canvas_(HTML)
[labs]: http://labs.alexanderae.com/jcanvas/
[json]: http://es.wikipedia.org/wiki/JSON
[easing]: http://gsgd.co.uk/sandbox/jquery/easing/
[easing-referencia]: http://easings.net/es
[docs]: http://calebevans.me/projects/jcanvas/docs/
[sandbox]: http://calebevans.me/projects/jcanvas/sandbox/
[github]: https://github.com/caleb531/jcanvas

[demo-01]: /static/pictures/jcanvas-01.png 'Jcanvas - demo 01'
[demo-02]: /static/pictures/jcanvas-02.png 'Jcanvas - demo 02'
[demo-03]: /static/pictures/jcanvas-03.png 'Jcanvas - demo 03'