Title: ¿Cómo encontrar imágenes similares con Python?
Date: 2019-11-24
Tags: imagenes, python
Slug: imagenes-similares-python
Author: __alexander__

## El problema: imágenes que no coinciden (y deberían coincidir)

Una de las tareas en <a href="https://librera.pe" target="_blank">Librera</a> implica recopilar la información de un libro en base a su ISBN, para lo cual en algunos casos se recurre al **webscraping**.

En algunos casos, al obtener la portada de un libro desde algún servicio externo como Google Books API, Goodreads API o scrapeando alguna web  verificábamos que obteníamos una portada incorrecta.

Nuestro proceso para obtener la portada de un libro implicaba:

1. Consultar varias fuentes (API's)
2. Escoger la portada en base al tamaño de la imagen, ya que un mayor tamaño, véase ancho x alto implicaba "mayor calidad".

<b>Nota:</b> No descargamos cada imagen, sino que tan solo verificábamos los primeros bits del archivo, ya que allí se encuentra información como las medidas de la misma.

Pero con el tiempo notamos que algunas portadas no coincidían por equis motivos (luego se vio que esto era un 0.005% o menos de las imágenes)

<br>
## La solución: comparar imágenes para encontrar coincidencias

Crear un script que descargue la portada de varias fuentes y las compare. La portada "escogida" además de tener el mayor tamaño, debe ser similar a alguna de las otras portadas, ya que es "altamente improbable" que el error se produzca entre varias fuentes.

Y es por ello que escribo este post, resumiendo mi pequeña investigación sobre el tema.

<br>
## Algoritmos para crear "hash" de imágenes

La comparación de las imágenes la podemos realizar de varias formas. En este caso, utilizaremos un hash[^1], que sería un *string* que actua a modo de resumen de cada imagen.

Los hash creados se deben caracterizar por:

- Ser únicos para cada imagen
- Si una imagen sufre una ligera variación, el hash resultante debe variar mínimamente también.

Para nuestras pruebas usaremos el cover del libro "Toda Mafalda":

![cover de toda mafalda][toda-mafalda]

Existen algunos algoritmos usualmente empleados en estos temas y son:

### Average Hash

El procedimiento del cálculo es el siguiente:

1. Generar una miniatura con tamaño fijo de la imagen: de este modo los cálculos serán más rápidos de realizar y los tamaños se homogenizan. Podemos trabajar con la medida de 8x8 con lo que tendremos 64 píxeles.

2. Reducimos los colores transformando la imagen a escala de grises.

3. Realizamos el cálculo de la media de los 64 valores

4. Ahora revisamos si cada bit es mayor o menor a la media, con lo que tendremos 64 bits (0 o 1)

5. Construimos el hash: transformamos la cadena de valores binarios a hexadecimal con lo que tendremos algo similar a: *ffffeff1e1e0661c *
    
![proceso de average hash][average-hash]

### Perceptual Hash

Debido a su implementación, el algoritmo de **Average Hash** es rápido y sencillo, pero también debido a su naturaleza, puede llegar a generar varios falsos positivos al momento de comparar imágenes similares cuando se realizan ajustes al "gama" de la imagen.

El proceso es:

1. Escalamos la imagen, pero a diferencia del algoritmo "Average Hash" se recomienda utilizar un mayor tamaño como "32x32"

2. Reducimos los colores transformando la imagen a escala de grises.

3. Calculamos la DCT o [Transformada de cosenos discreta][^2] 

4. Reducimos la DCT: El cálculo anterior nos brinda una matrix de 32x32, pero solo tomaremos los 8x8 píxeles del lado superior izquierdo, lo que nos representa las menores frecuencias

5. Calculamos el valor promedio (similar al algoritmo anterior)
6. Cálculamos el hash: establecemos los 64 bits en 0 o 1 según si cada valor supera o no el valor promedio calculado
7. Construimos el hash: transformamos la cadena de valores binarios a hexadecimal con lo que tendremos algo similar a: *e6cd90620d947bce*

### Otros algoritmos

Tenemos otros algoritmos que pueden ser revisados en las referencias al final del post como:

- Block Hash
- Diference Hash
- Wavelet Hash
- Median Hash

### ¿Cómo comparamos los hashes de las imaǵenes?

Para nuestras pruebas, ajustamos el brillo, contraste y escala de la imagen original para analizar los hashes:

![comparación de imágenes][imagenes_de_prueba]

Asumiendo que hemos calculado el hash escogido para nuestras imágenes, ¿cómo los comparamos?

Utilizamos un método conocido como **Distancia de Hamming**[^3].

Para las imágenes de prueba, los phash (perceptual hash) son:

        e6cd90620d947bce
        e6ed90e609947b8c
        
La distancia de hamming calcula el número de bits que deben cambiar entre dos cadenas para ser idénticas.

En este caso, el resultado es de "6", y al ser menor a 10 según algunos autores (*Dr. Neal Krawetz*) se podría decir que las imágenes son similares.

### Referencias

- <a href="http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html" target="_blank">Looks Like It - HackerFactor</a>
- <a href="https://fullstackml.com/wavelet-image-hash-in-python-3504fdd282b5" target="_blank">Wavelet image hash in Python</a>
- <a href="https://content-blockchain.org/research/testing-different-image-hash-functions/" target="_blank">Testing different image hash functions</a>
- <a href="https://www.pyimagesearch.com/2017/11/27/image-hashing-opencv-python/" target="_blank">Image hashing with OpenCV and Python</a>
- <a href="https://jenssegers.com/perceptual-image-hashes" target="_blank">Perceptual image hashes</a>


[^1]: <a href="https://es.wikipedia.org/wiki/Funci%C3%B3n_hash" target="_blank">Función hash - Wikipedia</a>
[^2]: <a href="https://es.wikipedia.org/wiki/Transformada_de_coseno_discreta" target="_blank">Transformada de cosenos discreta</a>
[^3]: <a href="https://es.wikipedia.org/wiki/Distancia_de_Hamming" target="_blank">Distancia de Hamming</a>


[toda-mafalda]: /pictures/hashing-images/toda_mafalda.jpg 'toda mafalda - librera.pe' 
[average-hash]: /pictures/hashing-images/toda_mafalda_comparacion.jpg 'average hash' 
[imagenes_de_prueba]: /pictures/hashing-images/toda_mafalda_prueba.jpg 'hashing de imágenes' 
