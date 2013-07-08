Title: Optimización de imágenes: Archivos PNG
Date: 2013-07-07 20:00
Tags: optimizacion, imagenes
Slug: optimizacion-de-imagenes-archivos-png
Author: __alexander__

#### Archivos PNG

Un problema recurrente al manejar este formato de archivos puede ser el hecho de que ocupen una mayor cantidad de espacio en disco y al ser junto a los archivos JPEG uno de los dos formatos más usados en el entorno web esto se puede traducir en mayor tiempo de carga para nuestros sitios web.

Como tal vez ya sepamos, los [PNG][PNG] son un formato de imágenes que soportan compresión sin pérdidas[^1]. Para entender el como funciona la *optimización* de las imágenes en este formato, debemos tomar en cuenta al proceso de *compresión*.

<br>
#### Compresión:

A modo de resumen, el archivo *png* se comprime en dos fases:

1. Filtrado: Una serie de filtros son escogidos para facilitar la compresión en la siguiente fase. Se utiliza un método de filtrado para ayudar a la predicción del color del pixel en base a sus vecinos.

2. El algoritmo de compresión utilizado en la segunda fase se denomina [deflate][deflate] el cual es el mismo algoritmo utilizado por la libreria [zlib][zlib].

Para mayor información, consulte la especificación de la norma [ISO][PNG-ISO].

<br>
#### Optimización:

La optimización de los archivos png se puede realizar:

- Eliminando los bloques auxiliares de la cabecera, los cuales pueden corresponder a información de los valores gama, el color de fondo, entre otros[^2].
- Utilizando una paleta de colores reducida ([paleta indexada][paleta-indexada])
- Optimizando los filtros linea a linea
- Optimizando la compresión mediante el método deflate.

- - -
#### Herramientas de optimización

De las múltiples posibilidades, decidí probar 3: pngcrush, optipng y pngquant:

##### PNGCrush

Proyecto opensource que se ejecuta por medio de la línea de comandos. Itera sobre los filtros y los parámetros usados por el método de compresión deflate, realizando la compresión para cada combinación posible y de este modo escoger la mejor alternativa.

Site: [pngcrush][pngcrush]

Modo de Uso:

        pngcrush -rem allb origen.png pngcrush.png

- - -
##### OptiPNG

Inspirado en base a pngcrush. Diseñado para ser mucho más veloz. A diferencia de *pngcrush*, *optipng* realiza las pruebas en memoria y escribe solo el resultado óptimo en el disco.

Site: [optipng][optipng]

Modo de Uso:

        optipng -o 2 origen.png -out optipng.png

- - -
##### PNGQuant

A diferencia de *pngcrush* y *optipng*, **pngquant** reduce el número de colores a utilizar (a 256 o menos). Por lo que si bien podemos lograr un tamaño mucho menor, es posible que se produzca una pérdida en la calidad.

Sitio: [pngquant][pngquant]

Modo de Uso:

        pngquant origen.png --ext -pngquant.png

Ejemplo: [tinypng.org][tinypng] (optimizador online que usa pngquant)

- - -
#### Comparativa

Comparando resultados para dos capturas de pantalla en formato png (las capturas están alojadas en google drive):

- Captura de pantalla del juego need for speed:

|Archivo |   [nfs.png][nfs.png] |   [pngcrush][nfs-pngcrush.png]    |  [optipng][nfs-optipng.png] | [pngquant][nfs-pngquant.png]
| -      |   -                  |   -                   |   -       | -
|Peso    |   2 MB               |   1.3 MB              |  1.3 MB   | 412 KB

- Captura de pantalla de la terminal:

|Archivo |   [consola.png][nfs.png] |   [pngcrush][consola-pngcrush.png]    |  [optipng][consola-optipng.png] | [pngquant][consola-pngquant.png]
| -      |   -                  |   -                   |   -       | -
|Peso    |   126.1 KB           |   105.0 KB            |  104.3 KB | 55.6 KB

- - -
#### Conclusiones

1. Aunque en la comparativa tan solo se aprecia el *espacio en disco* final, se debería de tomar en cuenta el *tiempo de procesamiento* de cada herramienta.

2. Si bien **pngquant** obtiene un tamaño considerablemente menor al original, se debe tener cuidado con su uso, ya que trabaja reduciendo la paleta de colores por lo que puede conllevar una pérdida en la calidad. (Para las dos imágenes mostradas el efecto es inapreciable)

3. Si mantener la calidad original es una prioridad, se recomienda el uso de **optipng**. Y en caso de que nos podamos permitir el reducir "levemente" la calidad[^3] podemos considerar el uso de **pngquant**.

- - -
#### Referencias

1. optipng: [A guide to PNG optimization][a-guide-to-png-optimization]
2. debianfacil.wordpress.com: [optimizando-y-reduciendo-imagenes-png][optimizando-y-reduciendo-imagenes-png]
3. [Portable Network Graphics][portable-network-graphics]
4. [Manpages Ubuntu][man-pngcrush]
5. [manual optipng][man-optipng]

[^1]: Se denomina algoritmo de compresión sin pérdida a cualquier procedimiento de codificación que tenga como objetivo representar cierta cantidad de información utilizando u ocupando un espacio menor, siendo posible una reconstrucción exacta de los datos originales.
Véase: [lossless data compression][lossless-data-compression]

[^2]: Consulte [PNG: Bloques auxiliares][png-bloques-auxiliares]

[^3]: Inapreciable para imágenes con pocos colores(<=256)

[PNG]: http://en.wikipedia.org/wiki/Portable_Network_Graphics
[deflate]: http://en.wikipedia.org/wiki/DEFLATE_(algorithm)
[zlib]: http://en.wikipedia.org/wiki/Zlib
[PNG-ISO]: http://tools.ietf.org/html/rfc2083
[paleta-indexada]: http://en.wikipedia.org/wiki/Indexed_color
[pngcrush]: http://pmt.sourceforge.net/pngcrush/index.html
[optipng]: http://optipng.sourceforge.net/
[pngquant]: http://pngquant.org/
[pngquant]: http://tinypng.org/

[lossless-data-compression]: http://en.wikipedia.org/wiki/Lossless_data_compression
[png-bloques-auxiliares]: http://en.wikipedia.org/wiki/Portable_Network_Graphics#Ancillary_chunks
[optimizando-y-reduciendo-imagenes-png]: http://debianfacil.wordpress.com/2008/03/18/optimizando-y-reduciendo-imagenes-png/
[a-guide-to-png-optimization]: http://optipng.sourceforge.net/pngtech/optipng.html
[portable-network-graphics]: http://www.libpng.org/pub/png/
[man-pngcrush]: http://manpages.ubuntu.com/manpages/raring/man1/pngcrush.1.html
[man-optipng]: http://linux.die.net/man/1/optipng

[nfs.png]: https://docs.google.com/file/d/0B9sAAyxUlH2tNTlPMmo5Vkk3R2c/edit?usp=sharing
[nfs-pngcrush.png]: https://docs.google.com/file/d/0B9sAAyxUlH2tWUhtUl9abjU2ZVE/edit?usp=sharing
[nfs-optipng.png]: https://docs.google.com/file/d/0B9sAAyxUlH2tc3Q5dDNYbi1vY2c/edit?usp=sharing
[nfs-pngquant.png]: https://docs.google.com/file/d/0B9sAAyxUlH2tVlJDWGpHX0U5YjA/edit?usp=sharing

[consola.png]: https://docs.google.com/file/d/0B9sAAyxUlH2tRGoxMi12QmZ2blU/edit?usp=sharing
[consola-pngcrush.png]: https://docs.google.com/file/d/0B9sAAyxUlH2tb1lzaXFQcnA3Wlk/edit?usp=sharing
[consola-optipng.png]: https://docs.google.com/file/d/0B9sAAyxUlH2tRHZDSy1RZXRFRHc/edit?usp=sharing
[consola-pngquant.png]: https://docs.google.com/file/d/0B9sAAyxUlH2tb1lzaXFQcnA3Wlk/edit?usp=sharing