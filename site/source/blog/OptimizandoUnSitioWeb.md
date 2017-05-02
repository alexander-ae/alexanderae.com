Title: Optimizando un sitio web 1
Date: 2017-05-01
Tags: optimizacion
Slug: optimizando-un-website-1
Author: __alexander__

Hace buen tiempo quería escribir sobre este tema, lo usual, de registro para mí y en el blog por si le ayuda a alguien más.

Un sitio web se puede optimizar en múltiples aspectos, pero para comenzar me voy a centrar en el lado del frontend y no sin antes indicar que estoy utilizando recomendaciones de múltiples recursos entre los que destacan [Google PageSpeed Insights][google_page_speed] y [Pingdom Website Speed Test][pingdom_test] y otros websites a los que voy a citar.


## ¿Por qué optimizar?

Tal vez ganar unos kilobytes o milisegundos por cada recomendación a seguir no parezca mucho pero en su conjunto, importan.

Cuántas veces me ha pasado que abandono un blog porque el tiempo de carga es lento ya sea por que estoy con una red limitada como la del celular o por el peso del propio website.
 
 Y así como me pasa, [estudios](https://blog.kissmetrics.com/loading-time/) indican que un visitante tiende a abandonar los sitios que identifica como lentos lo cuál se traduce en menos conversiones.

Entonces, ¿por qué?, diría que para brindar una mejor experiencia al usuario, porque ese usuario, podemos ser nosotros mismos en otro momento.

Claro, hay otras ventajas como un mejor posicionamiento en los buscadores, mejorar las conversiones o tan solo utilizar menos recursos del lado del servidor

## Mejoras en el frontend

### Minificar HTML, CSS y JS

Los espacios en blanco, saltos de línea y los comentarios pueden ocupar valiosos bytes.

Para removerlos pueden usar herramientas de postprocesamiento incorporadas en el framework o cms utilizado (plugins de wordpress) o con herramientas como gulp, grunt entre otros.

- [Google web developers: minificar recursos](https://developers.google.com/speed/docs/insights/MinifyResources?hl=es-419)

### Optimizar la entrega de webfonts

Al utilizar una 'web font' nos puede pasar que obtengamos:

- flash of invisible content: no vemos el texto hasta no descargar la tipografía
- flash of unstyled contend: vemos el texto pero este cambia su apariencia cuando al tipografía termina de descargar

Como muchos, recomiendo optimizarlo para el segundo caso, lo que se llama *progressive enhancement* mediante técnicas de lazy loading.

Existen otras formar de optimizar la entrega de tipografías como reducir el número de las mismas en la web o [entregar solo el subconjunto de caracteres](https://developers.google.com/fonts/docs/getting_started#specifying_script_subsets) que utilizaremos.

- [Google web font optimization](https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/webfont-optimization)
- [Web fonts, boy, I don't know](https://meowni.ca/posts/web-fonts/)


### Migrar a un stack de 'safe web fonts' o 'system fonts'

ya no estamos en el pasado cuando las tipografías por defecto de los sistemas operativos no eran 'agradables', ahora tenemos algunas opciones dentro de cada S.O. como:

- windows: calibri, tahoma, consolas
- macOS, iOS: helvetica, san francisco
- android: roboto, droid sans
- linux: ubuntu, oxygen

entonces, si podemos usar una fuente que viene instalada en el sistema, con la que el usuario está familiarizado y no tiene que descargar ningún extra ¿por qué no?

- [Moving to a System Font Stack in 2017][moving-to-a-system-font-stack] 
- [The new system font stack][new-system-font-stack]

### Habilitar la compresión de recursos

Además de minificar un archivo, también podemos comprimirlo mediante gzip. Esto generalmente se logra agregando unas cuantas líneas a la configuración de nuestro sevidor ya sea apache, nginx u otro.

- [Google: enable compression](https://developers.google.com/speed/docs/insights/EnableCompression)
- [Google: optimize encoding and transfer](https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/optimize-encoding-and-transfer)

### Optimizar imágenes

Las imágenes se pueden optimizar de diferentes maneras:

- mediante herramientas como: mozjpeg, optipng o gifsicle que recodifican la imagen, disminuyen la paleta de colores o una combinación de ambas.
- reemplazando la imagen original por otro formato, como puede ser un png por un archivo svg o un png por un jpeg
- utilizando webp
- reemplazando la imagen por un efecto css

Algunos recursos

- [Google image optimization][google_image_optimization]
- [Optimización de archivos PNG][alexander_png]
- [TinyPNG][TinyPNG]: herramienta online para comprimir jpg y png
- [Thumbor][thumbor]: servidor de imágenes opensource

### Reduce el tiempo de respuesta del servidor
Si bien, esta recomendación brindada por google tiene que ver con el backend, la anoto aquí por si alguien se pregunta el qué es.

Se refiere al tiempo que toma el servidor en procesar nuestra solicitud. Este tiempo puede verse afectado por factores como consultas SQL pesadas, renderizado de html, cálculos complejos entre otros.

### Especificar la caché del navegador

Mediante el uso de algunas cabeceras, el navegador nos permite indicarle el tiempo de expiración de un recurso.

Por ejemplo, la siguiente cabecera:

```
expires:Tue, 09 May 2017 00:07:05 GMT
```

Quiere decir que el recurso expira en la fecha indicada y hasta entonces no es necesario que el navegador lo vuelva a descargar al visitar nuevamente la página.

Esto se activa desde la configuración del servidor: apache o nginx

Por ejemplo, para agregar recursos estáticos a la cache de nginx podemos agregar algo similar a:

```
location ~* \.(?:ico|css|js|gif|jpe?g|png)$ {
    expires 7d;
}
```

- [Google Leverage Browser Caching](https://developers.google.com/speed/docs/insights/LeverageBrowserCaching)


### Elimina descargas innecesarias

Un buen ejemplo sería cuando el administrador de un website decide agregar un slide o carrousel con muchas imágenes sin preguntarse siquiera si el visitante se detendrá a revisar cada una de ellas.

Debemos evaluar si los recursos que utilizamos en una web son realmente utilizados, si compensa el costo de la descarga o tal vez podríamos prescindir de algunos.

- [Google: eliminate downloads](https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/eliminate-downloads)


## Notas finales

Algunas herramientas que pueden utilizar para medir el estado de un website son:

- [Google Page Speed][google_page_speed]
- [Pingdom Tools][pingdom_test]


Como observación final, indico que voy a tratar de mantener este artículo actualizado e iré añadiendo más recomendaciones con el tiempo.

[google_page_speed]: https://developers.google.com/speed/pagespeed/insights/
[pingdom_test]: https://tools.pingdom.com/

[google_image_optimization]: https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/image-optimization
[alexander_png]: https://alexanderae.com/optimizacion-de-imagenes-archivos-png.html
[TinyPNG]: https://tinypng.com/
[thumbor]: https://github.com/thumbor/thumbor

[moving-to-a-system-font-stack]: https://woorkup.com/system-font
[new-system-font-stack]: https://bitsofco.de/the-new-system-font-stack/
