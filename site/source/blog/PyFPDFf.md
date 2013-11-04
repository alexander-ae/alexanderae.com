Title: PyFPDF
Date: 2013-11-03
Tags: python
Slug: pyfpdf-un-generador-de-archivos-pdf-en-python
Author: __alexander__

PyFPDF es una librería[^1] que genera documentos PDF mediante python. Es un port de [FPDF][FPDF], el cual está escrito en PHP.

Mientras revisaba el código de este paquete (el cual no es muy complicado de entender, al menos en parte) hice un ejemplo en el que se hace uso del:

- encabezado y pie de página
- propiedades del documento (autor, título)
- manejo de tipografías (tamaño de texto y estilos incluidos)
- una tabla con contenidos de productos, cantidades y precios (similar a una boleta de compra).
- saltos de linea, celdas, imágenes, etc..

En gran parte tomé como referencia el código de ejemplo incluido en las fuentes del paquete, los cuales se pueden encontrar aquí: [pyfpdf][pyfpdf]

El código de mi generador de listas de compra fue el que sigue:

~~~
::python
from fpdf import FPDF


class PDF(FPDF):
    def config(self):
        self.set_author('__alexander__<alexander.ayasca.esquives@gmail.com>')
        self.set_title('Django Store: Boleta #1')
        self.alias_nb_pages(alias='pag_total')
        self.add_font('DroidSans', '', 'DroidSans.ttf', uni=True)
        self.add_font('DroidSans', 'B', 'DroidSans-Bold.ttf', uni=True)
        self.add_page()

    def header(self):
        # Encabezado
        self.image('logo.png', 10, 8, 32)  # Logo
        self.set_font('DroidSans', 'B', 15)  # Arial bold 15
        self.cell(80)  # Espacio en blanco de 8cm
        self.cell(40, 10, 'Django Store', 1, 0, 'C')  # Titulo
        self.ln(20)  # Salto de linea

    def footer(self):
        # Pie de pagina
        self.set_y(-15)  # margen inferior de 1.5cm
        self.set_font('DroidSans', '', 8)  # droidSans 8px
        # paginacion
        paginado = u'Pagina {0} de pag_total'.format(self.page_no())
        self.cell(0, 10, paginado, 0, 0, 'C')

    def parse_csv(self, csv_file):
        # Leemos los items del archivo csv y lo retornamos como un generador
        with open(csv_file, 'r') as f:
            for line in f:
                yield line.strip().split(';')  # recortamos los saltos de linea

    def fancy_table(self, header, data):
        # Dibuja la tabla de productos y precios
        # colores, ancho de linea y tipografia
        self.set_fill_color(255, 0, 0)
        self.set_fill_color(62, 255, 175)
        self.set_text_color(64)
        self.set_draw_color(128, 0, 0)
        self.set_line_width(.3)
        self.set_font('', 'B')
        # cabecera de la tabla
        w = [100, 25, 25, 30]
        for i in range(0, len(header)):
            self.cell(w[i], 8, header[i], 1, 0, 'C', 1)
        self.ln()

        #  restauramos el color y la tipografia para el contenido principal
        self.set_fill_color(170, 235, 210)
        self.set_text_color(32)
        self.set_font('')
        #  Data
        fill = 0
        total = 0
        for row in data:
            if len(row) > 3:
                # Solo si tenemos los valores de las 4 columnas en el csv
                self.cell(w[0], 7, row[0], 'LR', 0, 'L', fill)
                self.cell(w[1], 7, row[1], 'LR', 0, 'R', fill)
                self.cell(w[2], 7, '$' + row[2], 'LR', 0, 'R', fill)
                self.cell(w[3], 7, '$' + row[3], 'LR', 0, 'R', fill)
                self.ln()
                fill = not fill
                total = total + float(row[3])

        # pie de pagina de la tabla
        self.set_font('', 'B')
        self.cell(150, 7, 'Total:', 'LR', 0, 'R', fill)
        self.cell(30, 7, '$' + str(total), 'LR', 0, 'R', fill)
        self.ln()
        self.cell(sum(w), 0, '', 'T')  # linea final


if __name__ == '__main__':
    csv_file = 'boleta.csv'
    header = ['Producto', 'Cantidad', 'p x u', 'Subtotal']

    pdf = PDF()
    data = pdf.parse_csv(csv_file)

    pdf.config()

    pdf.fancy_table(header, data)
    pdf.output('boleta_1.pdf', 'F')

~~~

Se genera un pdf similar a:

![demo-img][demo-img]

El código anterior, asi como la imagen del logo, tipografías, archivo csv de entrada y el pdf generado se pueden descargar desde [aquí][ejemplo].

También, mientras revisaba el código de pyfpdf decidí realizar algunas anotaciones de los métodos que se pueden usar (ya que la documentación no es muy extensa). Y aunque solo tengo una parte terminada, la estoy colocando en [esta página][pyfpdf-doc].

[^1]: Mantenida por Mariano Reingart

[demo-img]: /static/pictures/boleta.png

[FPDF]: http://www.fpdf.org/
[pyfpdf]: https://code.google.com/p/pyfpdf/
[ejemplo]: http://owncloud.alexanderae.com/public.php?service=files&t=389c33821500c1f4598db7ddf2540d27
[pyfpdf-doc]: /pages/pyfpdf.html