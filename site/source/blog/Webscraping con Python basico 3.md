Title: Webscraping básico con Python - III
Date: 2019-12-04
Tags: webscrapping, python
Slug: webscrapping-python-3
Author: __alexander__

En esta ocasión, siguiendo el ejemplo del post anterior, realizaré la misma tarea pero utilizando <strong><a href='https://scrapy.org/' target='_blank'>Scrapy</a></strong>, un framework especializado en la tarea de realizar webscraping.

Nuestro objetivo es el mismo: descargar la lista de libros y precios de <a target='_blank' href='http://books.toscrape.com'>Books to scrape</a>.

## Requisitos

Necesitamos instalar *scrapy*:

> pip install scrapy
        
### Comenzando

Nuestro script, según el ejemplo de la documentación de *scrapy*, toma la siguiente forma:

~~~
::python
import scrapy

url = 'http://books.toscrape.com'


class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = [
        url,
    ]

    def parse(self, response):
        for book in response.css('.product_pod'):
            yield {
                'title': book.css('h3 a').attrib['title'],
                'price': book.css('p.price_color::text').get()[1:],
            }
~~~

Y ejecutamos el código con:

> scrapy runspider books.py -o books.csv
    
## ¿Cómo interpreta scrapy lo anterior?

Scrapy inicia consultando los enlaces en *start_urls*, en este caso solo es un enlace, y posteriormente, ejecuta el método *"parse"*, enviándole el objecto *"response"* como parámetro.

Dentro del método *parse*, utilizamos selectores CSS mediante la librería *parsel*, la cual actua de alternativa a *beautifulsoup*.

Nótese que mediante la línea de comandos también indicamos el archivo de salida en formato CSV. Scrapy soporta los siguientes formatos de forma nativa: JSON, XML y CSV.

### Iterando sobre las páginas

Si se observa el archivo de resultado, veremos que scrapy solo retorna los resultados de la primera página. Para ellos

Actualizando el código para considerar la paginación, quedaría del siguiente modo:

~~~
::python
import scrapy

url = 'http://books.toscrape.com'
prefix_page = 'catalogue'


class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = [
        url,
    ]

    def parse(self, response):
        for book in response.css('.product_pod'):
            yield {
                'title': book.css('h3 a').attrib['title'],
                'price': book.css('p.price_color::text').get()[1:],
            }

        next_page = response.css('.pager .next a').attrib['href']
        if next_page:
            if prefix_page in next_page:
                next_url = '{}/{}'.format(url, next_page)
            else:
                next_url = '{}/{}/{}'.format(url, prefix_page, next_page)

            yield response.follow(next_url, self.parse)

~~~

Y al ejecutar lo anterior nuevamente:

> scrapy runspider books.py -o books.csv

obtendríamos de resultado los 1000 libros que existen en la página.


### Conclusión

Scrapy resulta una herramienta muy práctica ya que:

- Tiene soporte nativo para selectores CSS
- Soporte nativo para generar archivos de salida (CSV, JSON)
- Permite rotar el "User Agent"
- Permite agregar una demora entre descargas para no sobrecargar las páginas a scrapear (DOWNLOAD_DELAY)
- Incluye una herramienta que realiza un benchmark a nuestro proceso

### Publicaciones anteriores

1. <a target='_blank' href='https://docs.scrapy.org/en/latest/intro/overview.html'>Webscraping básico con Python - I</a>

2. <a target='_blank' href='https://parsel.readthedocs.io/en/latest/usage.html'>Webscraping básico con Python - II</a>

### Referencias

* Documentación de <a target='_blank' href='https://www.crummy.com/software/BeautifulSoup/bs4/doc/'>Scrapy</a>

* Documentación de <a target='_blank' href='https://requests.readthedocs.io/en/master/'>Parsel</a>
