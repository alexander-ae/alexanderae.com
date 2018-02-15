Title: Herramientas para extraer texto de archivos PDF
Date: 2018-02-12
Tags: pdf
Slug: extraccion-de-texto-desde-pdf
Author: __alexander__

Algunos casos de uso en los que se requiera extraer texto de archivos pdf pueden ser:

- ejecutar análisis de curriculums vitae (hojas de vida)
- para permitir la búsqueda por contenidos en un archivo
- obtención de los datos de contacto de empresas desde boletas o facturas de pago
- conversión a un formato más amigable para su presentación en la web (html) entre otros

A continuación, 3 herramientas que se pueden utilizar para extraer texto de archivos PDF:

## 1. PDFMiner (python):

**Enlace**: [pdfminer-six][pdfminer-six] 

** Instalación **:

`pip install pdfminer.six`

** Uso **:

`pdf2txt.py archivo.pdf`

** Características resaltantes **:

- permite escoger el formato de salida: txt, xml, html
- selección del rango de páginas a escanear
    
## 2. Apache Tika (java):

Apache tika es una herramienta que extrae metadatos y texto desde varios formatos como: doc, ppt, xls, pdf entre otros

** Enlace **: [apache-tika][apache-tika]

** Instalación y uso **:

Se requiere contar con java instalado, descargar tika y ejecutarlo de forma similar a:

`java -jar tika-server.jar`

** Características **

- reconoce múltiples formatos de entrada
- permite escoger el formato de salida: txt, xml, html
- extracción de metadata: cantidad de páginas, versión de pdf, extensión del documento, número de páginas entre otros.
- cuenta con una herramienta gráfica: *tika-app.jar* que se puede utilizar para realizar pruebas de forma rápida
- existe un wrapper para utilizarlo con python: [tika-python][tika-python]


## 3. pdftotxt (linux)

Herramienta para extraer pdf incluida por defecto en varias distribuciones linux.

** Documentación **: [pdftotext][pdftotext]

** Uso **

`pdftotext documento.pdf`

Con lo anterior, se crea el archivo: *documento.txt*

** Características **

- selección del rango de páginas a escanear
- es la más sencilla de utilizar ya que viene preinstalada

- - -

## Comentarios finales

- En general, quien me ha brindado mejores resultados para pdf's complejos ha sido **apache tika** y pdftotext para documentos sencillos.

- Si lo que se busca es extraer imágenes de un PDF, en mi caso [PDFBox][PDFBox] me ha dado buenos resultados también.

## Referencia:

- Tools for Extracting Data and Text from PDFs - A Review: [tools-for-extracting-data][tools-for-extracting-data]


[pdfminer-six]: https://github.com/pdfminer/pdfminer.six
[apache-tika]: https://tika.apache.org/
[tika-python]: https://github.com/chrismattmann/tika-python
[pdftotext]: https://www.mankier.com/1/pdftotext
[PDFBox]: https://pdfbox.apache.org/
[tools-for-extracting-data]: http://okfnlabs.org/blog/2016/04/19/pdf-tools-extract-text-and-data-from-pdfs.html