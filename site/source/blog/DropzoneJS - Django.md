Title: Dropzone + Django
Date: 2014-10-19
Tags: django, js
Slug: dropzonejs-django
Author: __alexander__
Summary: DropzoneJS es una libreria opensource que permite subir archivos mediante la acción 'arrastrar y soltar' con la capacidad de mostrar vistas previas de las imágenes. Y django.. bueno, ya sabemos qué es django.


> [DropzoneJS][DropzoneJS] es una libreria opensource que permite subir archivos mediante la acción "arrastrar y soltar" con la capacidad de mostrar vistas previas de las imágenes.

Para este ejemplo utilicé [django][django] 1.7 + Python 2.7, pero no debería existir ningún problema para utilizarlo con otras versiones.

- - -

Los pasos que realicé, en resumen son:

*1.* Descargar el último *[release][dropzone-release]* y añadirlo a nuestro directorio de archivos *static*.

*2.* Creamos el modelo:

~~~
::python
class Picture(models.Model):
    imagen = models.ImageField("Imagen", upload_to='imagenes')
~~~

*3.* .. el formulario:

~~~
::python
class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = ('imagen',)
~~~

*4.* .. la url:

~~~
::python
url(r'^upload-picture/$', 'upload_picture', name='upload_picture'),
~~~

*5.* .. el view:

~~~
::python
from django.shortcuts import render_to_response as render
from django.template import RequestContext as ctx

from .forms import PictureForm


def upload_picture(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)

        if form.is_valid():
            picture = form.save()
    else:
        form = PictureForm()

    return render("upload_picture.html", locals(), ctx(request))
~~~

*6.* Y por último, el template "upload_picture.html":

~~~
::html
{% load static %}

<html>
    <head>
        <link rel="stylesheet" href="{% static 'dropzone/css/dropzone.css' %}">
    </head>

    <body>
        <form action="{% url 'upload_picture' %}" class="dropzone" id="myDropzone" method='POST' enctype="multipart/form-data">
            {% csrf_token %}

            <div class="fallback">
                <input name="file" type="file" multiple />
            </div>
        </form>

        <script src="{% static 'dropzone/dropzone.min.js' %}"></script>
        <script type="text/javascript">
            Dropzone.options.myDropzone = {
                paramName: "imagen", // el nombre de nuestro input
                autoProcessQueue : true,
                parallelUploads: 1,

                init: function() {
                    this.on("success", function(file, responseText) {
                        // evento lanzado al terminar de subir las imágenes en cola
                        console.log(responseText);
                    });
                }
            };
        </script>
    </body>
</html>
~~~

- - -

Tan sencillo como eso.

Nota: tomé como referencia a este post ["DropzoneJs + Django: How to build a file upload"][dropzone-django]

[DropzoneJS]: http://www.dropzonejs.com/
[django]: https://www.djangoproject.com/
[dropzone-release]: https://github.com/enyo/dropzone/releases
[dropzone-django]: http://amatellanes.wordpress.com/2013/11/05/dropzonejs-django-how-to-build-a-file-upload-form/