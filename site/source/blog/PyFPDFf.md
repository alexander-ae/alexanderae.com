Title: PyFPDF
Date: 2013-07-21
Tags: python
Slug: pyfpdf-un-generador-de-archivos-pdf-en-python
Author: __alexander__
status: draft

PyFPDF es una librería que genera documentos PDF mediante python. Es un port de [FPDF][FPDF].

#### Instalación:

        pip install fpdf

#### Ejemplo

Tal y como se observa en el tutorial[^1], un ejemplo sencillo es el siguiente:

~~~
::python

from fpdf import FPDF
pdf=FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(40, 10, 'Hola Mundo!')
pdf.output('tuto1.pdf', 'F')
~~~

#### Uso

El objeto base FPDF() acepta los siguientes parámetros con los valores por defecto indicados:

orientation='P', unit='mm'y format='A4'

que corresponden a:

*orientation*: orientación del documento

    'p' o 'portrait': vertical
    'l' o 'landscape': horizontal

*unit*: unidades a usar
    'pt': puntos
    'mm': milimetros
    'cm': centimetros
    'in': pulgadas

recordando que: 1 pulgada equivale a 72 puntos[^2]

*format*: formato de hoja, cuyos posibles valores son:

    'a3', 'a4', 'a5', 'letter' y 'legal'


- - -

##### Ajustes adicionales:

es posible realizar los ajustes indicados a continuación mediante los métodos del objeto FPDF respectivos:

1. *márgenes*:

    set_margins(left,top,right=-1)

    set_left_margin(margin)

    set_top_margin(margin)

    set_right_margin(margin)

2. *salto de página*:

    el salto de página para cuando se trabaja con celdas, multiceldas o imágenes, si el objeto va por debajo del límite inferior, se crea una nueva hoja.

        set_auto_page_break(auto, margin=0)

    Parámetros:

    - auto: booleano que indica si se activa o no el salto de página.
    - margin: distancia desde el tope inferior de la página a la que se activa el salto de línea.

    tambien podríamos sobreescribir el método *accept_page_break*[^3] si es que usamos una clase que herede de FPDF.

3. *zoom y vista de página*:

    el zoom y la vista de página por defecto se controlan[^4] por medio del método:

        set_display_mode(zoom, layout=continuous)

    El zoom acepta como valores a: fullpage, fullwidth o real.

    La vista de página (layout) acepta como valores a: continuous, two o default.

4. *compresión*:

    Habilita la compresión mediante zlib:

        set_compression(compress)

    compress: True o False

5. *Título, Asunto, Autor, Palabras clave, Creador*:

    set_title(title)
    set_subject(subject)
    set_author(author)
    set_keywords(keywords)
    set_creator(creator)

6. *Nueva página*:

    add_page(orientation='')

7. *Encabezado y pie de página*

    header() y footer(): son dos métodos que permiten insertar el encabezado y pie de página. Ambos son llamados automáticamente al crear una nueva página por el método add_page(). Para ser utilizados debe de utilizarse una subclase de FPDF e implementar los métodos anteriores.


        class PDF(FPDF):
            def header(self):
                # Tipo de fuente
                self.set_font('Arial','B',15)
                # Alineación de 80 espacios
                self.cell(80)
                # Tìtulo
                self.cell(30,10,'Title',1,0,'C')
                # Salto de línea
                self.ln(20)

8. *Ajustes de colores y dibujo*:

    set_draw_color(r, g, b): color de trazos

    set_fill_color(r, g, b): color de relleno

    set_text_color(r, g, b): color de texto

    set_line_width(width): ancho de linea

9. *Lineas y figuras*:

    *line(x1, y1, x2, y2)*: dibuja una línea

    *dashed_line(x1, y1, x2, y2, dash_length=1, space_length=1)*: dibuja una línea punteada, permite indicar la longitud de los guiones y el espacio entre ellos.

    *rect(x, y, w, h, style='')*: dibuja un rectángulo

    - x, y: límite izquierdo superior
    - w, h: ancho y alto
    - style: puede tomar los valores de 'F', 'FD', 'DF' y 'S'. Si bien en la documentación no encontré el qué hacia cada valor, por lo que pude probar:

        - 'F': no dibuja los bordes del rectángulo
        - 'FD' y 'DF': dibujan los bordes
        - 'S': solo dibuja los bordes

10. *Manejo de fuentes (tipos de letra)*:

    *[add_font][docs_add_font](family, style='', fname='', uni=False)*: importa una fuente y la hace disponible para su uso.

    - family: es el álias a utilizar para la fuente importada. Este valor es utilizado por *set_font*.
    - style: valor sin uso, se mantiene por compatibilidad.
    - fname: nombre del archivo fuente('DejaVuSansCondensed.ttf'). Es posible también, indicar la ruta completa, en ese caso se buscará el archivo en FPDF_FONTPATH or SYSTEM_TTFONTS (variables de entorno).
    - uni: [flag][flag] que indica si la fuente soporta valores unicode o no.

    por ejemplo:

        # Añade una fuente unicode
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)

        # Añade una fuente unicode del sistema, usando su ruta completa
        pdf.add_font('sysfont', '', r'c:\WINDOWS\Fonts\arial.ttf', uni=True)

    *[set_font][docs_set_font](family, style='', size=0)*: Ajusta la fuente usada para imprimir los textos. Es necesario llamar a este método añ menos una vez antes de imprimir textos o el documento resultante será inválido.

    - family: familia de la fuente, corresponde al nombre usado con el método  *add_font*.
    - style: estilo de fuente, puede ser:

        - cadena vacía(''): regular
        - 'B': negrita
        - 'I': Itálica o Cursiva
        - 'U': Subrayado
        - Cualquier combinación de las anteriores, por defecto se usa el estilo regular.

    - size: tamaño en puntos, el valor por defecto es 12.

    por ejemplo:

        # Times regular 12
        pdf.set_font('Times')
        # Arial bold 14
        pdf.set_font('Arial','B',14)
        # Se remueve el estilo 'negrita'
        pdf.set_font('')
        # Times en negrita, italica y subrayado con 14 puntos
        pdf.set_font('Times','BIU')

    *set_font_size(size)*: ajusta el tamaño de la fuente usada

    *get_string_width*(s): obtiene el ancho ocupado por el texto indicado en la fuente actual.

Utilidades.



[^1]: El cual se puede ver en su [wiki][wiki-pyfpdf]
[^2]: también llamado [punto postscript][punto] o punto tipográfico
[^3]: retorna un booleano que indica si se debe o no saltar de página.
[^4]: he probado este método en okular (visor de kde) sin resultados, espero probarlo en acrobat reader.

[FPDF]: http://www.fpdf.org/
[wiki-pyfpdf]: https://code.google.com/p/pyfpdf/wiki/Tutorial
[punto]: http://es.wikipedia.org/wiki/Punto_tipogr%C3%A1fico
[docs_add_font]: https://code.google.com/p/pyfpdf/wiki/AddFont
[docs_set_font]: https://code.google.com/p/pyfpdf/wiki/SetFont
[flag]: http://es.wikipedia.org/wiki/Flag