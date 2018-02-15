Title: Análisis de legibilidad de textos
Date: 2018-02-14
Tags: analisis-de-textos, accesibilidad, ux
Slug: analisis-de-legibilidad-de-textos
Author: __alexander__

Al parecer en el inglés existen dos palabras que hacen referencia a la facilidad para leer un texto[^1]:

- legibility: legibilidad tipográfica, que se refiere a la tipografía (aspecto visual del texto)
- [readability][readability]: legibilidad lingüistica, que se refiere a la estructura lingüistica como el número de palabras que se usan y la forma en las que se combinan.

Este artículo trata sobre la fórmula necesaria para calcular la *legibilidad lingüistica* y su implementación en python[^2].

- - -

Medir la *legibilidad* de textos en español puede ser requerido para:

- evaluar la edad necesaria para comprender un texto
- calcular qué tan sencillo de entender será para nuestro público objetivo
- calcular tiempos de lectura

Algunas de las fórmulas aplicables al español son:

- Escala INFLESZ (2008)
- Legibilidad µ (2006)
- Nivel de perspicuidad - Szigriszt-Pazos (1993)
- Nivel de Comprensibilidad - Crawford (1989)
- Nivel de comprensibilidad - Gutiérrez de Polini (1972)
- Escala de lecturabilidad - Fernández Huerta (1959)

En este caso solo calcularemos la escala *INFLESZ*[^3], la cual requiere obtener el índice *Flesh-Szigriszt*:

    Índice FLESCH-SZIGRISZT = 206,835 – (62,3 x S/P ) - P/F 

Donde P es el número de palabras del texto, S el número de
sílabas y F es el número de frases. 

**Escala Inflesz:**

| Puntos | Grado | Tipo de Publicación |
| ---------- | ---------- | ---------- |
| < 40   | Muy difícil   | Universitario, Científico |
| 40 - 55| Algo difícil   | Bachillerato, Divulgación, Científico, Prensa especializada |
| 55 - 65| Normal   | ESO, Prensa general, Prensa deportiva |
| 65 - 80| Bastante fácil   | Educación primaria |
| > 80 | Muy fácil | Educación Primaria, Cómic |

Para llegar a lo anterior debemos dividir el problema, por lo cual necesitaremos:

**1.** el número de palabras de un texto: lo podemos obtener de la siguiente manera:

~~~~
::python
def count_words(text):
    return len(text.split())
~~~~

**2.** el número de sílabas de una palabra: este punto es un tanto más complejo porque requiere utilizar las reglas del español para dividir sílabas, para nuestro caso la referencia es: [https://github.com/mabodo/sibilizador](https://github.com/mabodo/sibilizador)

**3.** el número de frases de un texto: utilizamos una expresión regular para agrupar los separadores como puntos, comas, dos puntos, entre otros. Luego utilizamos el método split de un objeto regex para separar las frases y las contamos.

~~~~
::python
def count_sentences(text):
    text = text.replace("\n", "")
    sentence_end = re.compile('[.:;!?\)\()]')
    sencences = sentence_end.split(text)
    return len(list(filter(None, sencences)))
~~~~

Y con esto, ya solo quedaría unir los bloques para lograr el cálculo deseado. Se puede ver el script original en python en [github][github-inflesz] o la versión que empaqueté para [pypi][pypi-legibilidad].

## Más información
 
- [Código del paquete en pypi][pypi-legibilidad]
- [legible.es][legible]: web con información sobre análisis de legibilidad de textos en español
- [Legibility, Readability, and Comprehension: Making Users Read Your Words][nngroup-legibility]: análisis del impacto de la legibilidad en la experiencia de usuario

[^1]: [Diferencia entre readability y legibility](https://www.proz.com/kudoz/english_to_spanish/psychology/3583621-legibility_and_readability.html)
[^2]: Me baso en el script publicado por Alejandro Muñoz en su blog: [legible.es][legible]
[^3]: Inés Barrio, 2007, [Legibilidad y salud](https://legibilidad.blogspot.pe/). Tésis doctoral. pag 289

[github-inflesz]: https://github.com/amunozf/legibilidad
[pypi-legibilidad]: https://gitlab.com/__alexander__/legibilidad
[readability]: https://en.wikipedia.org/wiki/Readability
[legible]: https://legible.es/
[nngroup-legibility]: https://www.nngroup.com/articles/legibility-readability-comprehension/
