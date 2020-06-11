Title: Capturar la pantalla con Python (Selenium)
Date: 2020-06-10
Tags: python,
Slug: capturas-pantalla-python-selenium
Author: __alexander__
Summary: En el siguiente post veremos cómo obtener capturas de pantalla de websites con Selenium. Selenium es una herramienta utilizada para automatizar la interacción con los navegadores.

Sabemos que en Python podemos obtener el código de HTML de una página web con muchas herramientas como: urllib, requests, faster_than_requests entre otras, pero para **renderizar** el contenido de un website, necesitamos herramientas como **selenium**.

<a href="https://www.selenium.dev/" target="_blank">Selenium</a> es un entorno de pruebas para websites, el cual nos permite automatizar muchas tareas relacionadas al uso de un navegador mediante código.

Para nuestro ejemplo, necesitaremos dos cosas:

1. Instalar selenium

        pip install selenium
        
2. Instalar <a href="https://chromedriver.chromium.org/" target="_blank">chomedriver</a>, el driver oficial para manipular Chrome.

    Para ello debemos descargar el driver de la página oficial según nuestro sistema operativo, y agregar el directorio que lo contiene al PATH.

**Nota:** debemos descargar la versión adecuada según la versión de nuestro navegador.

<br>
## El código

Ahora podemos escribir el código necesario. Noten que usaremos chrome en su versión <a href="https://developers.google.com/web/updates/2017/04/headless-chrome" target="_blank">headless</a>, de este modo podemos interactuar con el navegador en entornos donde no necesitamos su interfaz gráfica.

~~~
::python
from selenium import webdriver

url = 'https://www.djangoproject.com/'
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1024,768')
options.add_argument('--headless')
options.add_argument('--disable-gpu')

browser = webdriver.Chrome(options=options)

browser.get(url)
browser.save_screenshot('django.png')
browser.close()
~~~

Lo que nos produce la siguiente salida:

![captura de la página de Django](/pictures/selenium_django.png)
 
 Notamos el uso de algunos parámetros como:
 
 * --windows-size: para ajustar el tamaño de la ventana a capturar
 * --headless: para que chrome se ejecute sin necesidad de iniciar la interfaz gráfica
 * --disabled-gpu: parámetro necesario si usamos Windows como sistema operativo.
 
 **Nota:** podemos deshabilitar la visualización del scrollbar con la opción extra *--hide-scrollbars*

<br>
## Tomando una captura de la página completa

En la captura anterior, se observa que solo fue tomada una sección de la página. ¿Cómo podemos capturar la pantalla completa del navegador?

Para ello podemos ejecutar un código javascript para conocer el tamaño de la página y tomar una nueva captura:

~~~
::python
import time
from selenium import webdriver

url = 'https://www.djangoproject.com/'
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1024,768')
options.add_argument('--headless')
options.add_argument("--hide-scrollbars")
options.add_argument('--disable-gpu')

browser = webdriver.Chrome(options=options)
browser.get(url)
time.sleep(2)  # esperamos que cargue todo con un tiempo moderado
height = browser.execute_script(
    "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
print(height)
browser.close()

# realizamos la captura con el "alto" que hemos obtenido
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument(f'--window-size=1024,{height}')
options.add_argument('--headless')
options.add_argument("--hide-scrollbars")
options.add_argument('--disable-gpu')
options.add_argument('--ignore-certificate-errors')

browser = webdriver.Chrome(options=options)
browser.get(url)
browser.save_screenshot('django_fullpage.png')
~~~

Si, así de simple.

<br>
## Observaciones finales

Como hemos visto, con selenium podemos automatizar el proceso de tomar capturas. Un usuario podría ingresar una url en nuestro sistema y mediante lo anterior, podríamos realizar una captura.

Claro, con selenium podemos automatizar muchas otras tareas como darle click a botones, testear formularios u otros, por lo que recomiendo darle una revisión para conocer todas las posibilidades.
 