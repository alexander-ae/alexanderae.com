Title: Webscraping básico con Python - II
Date: 2019-12-01
Tags: webscraping, python
Slug: webscraping-python-2
Author: __alexander__

Continuando con un post realizado hace unos meses sobre los fundamentos del webscraping: <a target='_blank' href='https://alexanderae.com/webscraping-python.html'>Webscraping básico con Python - I</a>, en esta ocasión presento otro ejemplo práctico para obtener información de un website.

Para nuestra pruebas utilizaremos <a target='_blank' href='http://books.toscrape.com'>Books to scrape</a>, una página que simula ser una librería, creada con fines educativos por ScrapingHub[^1].

Dicha web cuenta con:

- 1000 items en total
- Paginación
- 20 items por página
- No requiere javascript para leer el contenido

## Requisitos

Necesitamos tener instaladas los siguientes paquetes:

- beautifulsoup4: facilita el scraping de websites permitiendo acceder a los elementos HTML de una página de forma sencilla 
- lxml: HTML parser
- requests: permite realizar consultas HTTP 

## El problema

A modo de ejemplo, intentaremos obtener la información de los libros tales como título y precios.

### Comenzando

Nuestro script de forma inicial podría tomar la siguiente forma:

~~~
::python
import requests

url = 'http://books.toscrape.com'

content = requests.get(url)
print(content.text)
~~~

Lo indicado anteriormente tan solo obtiene el contenido del Home (la pantalla inicial).


### Listando las páginas

Analizando la página observamos que la paginación  en la sección inferior cuenta con los botones "previous" y "next".

El enfoque que tomaremos será obtener el enlace "next", redirigirnos hacia aquella página y buscar el nuevo enlace "next". En caso de que no exista una página siguiente, nos detenemos.

Notemos que <b>"next_url"</b> se construye de dos maneras porque en la página 1 el enlace es del tipo <b>"catalogue/page-2.html"</b> mientras que en la página 2 hacia adelante es del tipo <b>"page-3.html"</b>.

~~~
::python
import requests
from bs4 import BeautifulSoup


url = 'http://books.toscrape.com'
prefix_page = 'catalogue'

def obtiene_paginas():
    response = requests.get(url)
    
    while True:
        soup = BeautifulSoup(response.text, 'lxml')
        next_page = soup.select('.pager .next a')
    
        if next_page:
            if prefix_page in next_page[0].get('href'):
                next_url = '{}/{}'.format(url, next_page[0].get('href'))
            else:
                next_url = '{}/{}/{}'.format(url, prefix_page, next_page[0].get('href'))
            print(next_url)
            response = requests.get(next_url)
        else:
            break

if __name__ = '__main__':
    obtiene_paginas()
~~~

### Obtenemos los libros y sus precios

Cada página tiene un listado de libros, a su vez, cada libro está en un bloque con una clase CSS: <b>"product_pod"</b>

~~~
::python
def get_books(soup):
    books = []
    html_books = soup.select('.product_pod')
    for html_book in html_books:
        books.append({
            'title': html_book.select('h3 a')[0]['title'],
            'price': html_book.select('.price_color')[0].get_text()[2:]
        })
~~~

Note que para el precio, estamos comenzando desde el caracter número 3 ([2:]) ya que los 2 primeros caracteres contienen información no relevante.

### Grabando los resultados en una archivo CSV

Un archivo CSV, es un archivo de texto con valores separados por comas que representan datos en forma de tabla.

Escribimos una función que reciba la lista de libros y las escriba al final de un archivo CSV, de tal forma que nuestro código queda similar a:

~~~
::python
def export_to_csv(books):
    with open('books.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        for book in books:
            csvwriter.writerow((book['title'], book['price']))
~~~


### Resultado

Nuestro código finalmente quedará del siguiente modo:
~~~
::python
import csv
from datetime import timedelta
from timeit import default_timer as timer

import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com'
prefix_page = 'catalogue'


def get_pages():
    response = requests.get(url)

    while True:
        soup = BeautifulSoup(response.text, 'lxml')
        books = get_books(soup)
        export_to_csv(books)
        next_page = soup.select('.pager .next a')

        if next_page:
            if prefix_page in next_page[0].get('href'):
                next_url = '{}/{}'.format(url, next_page[0].get('href'))
            else:
                next_url = '{}/{}/{}'.format(url, prefix_page, next_page[0].get('href'))
            print(next_url)
            response = requests.get(next_url)
        else:
            break


def get_books(soup):
    books = []
    html_books = soup.select('.product_pod')
    for html_book in html_books:
        books.append({
            'title': html_book.select('h3 a')[0]['title'],
            'price': html_book.select('.price_color')[0].get_text()[2:]
        })

    return books


def export_to_csv(books):
    with open('books.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        for book in books:
            csvwriter.writerow((book['title'], book['price']))


if __name__ == '__main__':
    start = timer()
    get_pages()
    end = timer()
    print(timedelta(seconds=end - start))
~~~

Noten que hemos añadido un contador para conocer cuánto tiempo demora nuestro código en ejecutarse.

Si se ejecuta el script, podremos notar que el documento CSV creado contiene los 1000 libros que extrajimos desde la página de prueba.

### Posibles mejoras

Un tip rápido para mejorar los tiempos de procesamiento es el de reemplazar la librería **requests** por: <a target='_blank' href='https://github.com/juancarlospaco/faster-than-requests'>Faster-than-Requests
</a>

En mi caso, el tiempo de ejecución total se redujo a la mitad con tan solo el reemplazar la librería.

### Referencias

* Documentación de <a target='_blank' href='https://www.crummy.com/software/BeautifulSoup/bs4/doc/'>BeautifulSoup</a>

* Documentación de <a target='_blank' href='https://requests.readthedocs.io/en/master/'>requests</a>

* Documentación de <a target='_blank' href='https://docs.python.org/3/library/csv.html#csv.writer'>Python para manipular archivos CSV</a>

[^1]: <a target='_blank' href='https://scrapinghub.com/'>ScrapingHub</a> es una empresa dedicada a brindar servicios de webscraping.
