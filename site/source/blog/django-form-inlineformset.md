Title: Django: Ejemplo de Form + InlineFormset
Date: 2015-02-23
Tags: django, tutorial
Slug: django-form-inlineformset
Author: __alexander__
Summary: A modo de práctica con los Form + Formset desarrollaré una aplicación para registrar recetas con sus respectivos ingredientes y procedimientos. El propósito será poder editar todo el detalle de una receta incluidos los ingredientes y procedimiento en la misma pantalla, de modo similar a como se trabaja en el admin de django con los inlines.


A modo de práctica con los Form + Formset desarrollaré una aplicación para registrar recetas con sus respectivos ingredientes y procedimientos [^1].

El propósito será poder editar todo el detalle de una receta incluidos los ingredientes y procedimiento en la misma pantalla, de modo similar a como se trabaja en el admin de django con los inlines [^2].

#### 1. MODELS

Necesitaremos 3 modelos: recetas, ingredientes y procedimientos.

~~~
::python
# models.py
from django.db import models


class Receta(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()


class Ingrediente(models.Model):
    receta = models.ForeignKey(Receta)
    descripcion = models.CharField(max_length=255)


class Instruccion(models.Model):
    receta = models.ForeignKey(Receta)
    numero = models.PositiveSmallIntegerField(help_text='Paso número')
    descripcion = models.TextField()

~~~

Como se ve, nada complicado para comenzar. El modelo "principal" es el de la receta. Tenemos también a los modelos `Ingrediente` e `Intrucción` con sus respectivos `Foreign Key`.

#### 2. FORM:

Necesitamos un formulario para la receta:

~~~
::python
# forms.py
from django import forms
from .models import Receta


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
~~~


#### 3. URL's

Necesitamos 3 url's para: el listado de recetas, registro y edición de las mismas.

~~~
::python
# urls.py
..
url(r'^$', 'recetas.views.recetas', name='lista'),
url(r'^recetas/registrar/$', 'recetas.views.registro_edicion', name='registrar'),
url(r'^recetas/(?P<receta_id>\d+)/$', 'recetas.views.registro_edicion', name='editar'),
~~~

#### 4. VIEWS

Creamos dos vistas, una para listar nuestras recetas y la otra para manejar el registro y edición de las mismas.

Lo "complicado" se ve en la segunda vista:

- Obtenemos una instancia de la receta actual en caso de que la estemos editando o creamos una nueva para el caso de un registro.
- Inicializamos los dos [InlineFormset][django-inlineformset], uno para los ingredientes y otro para las instrucciones.
- En caso de que sea un pedido POST, validamos el formulario y los inlineformset, de ser válidos grabamos los cambios.
- En caso de que sea un GET, inicializamos el form y los 2 formsets.

~~~
::python
# views.py
from django.shortcuts import render_to_response as render, redirect
from django.template import RequestContext as ctx
from django.forms.models import inlineformset_factory

from .models import Receta, Ingrediente, Instruccion
from .forms import RecetaForm


def recetas(request):
    recetas = Receta.objects.all()

    return render('recetas.html', locals(),
        context_instance=ctx(request))


def registro_edicion(request, receta_id=None):
    if receta_id:
        receta = Receta.objects.get(pk=receta_id)
    else:
        receta = Receta()

    IngredienteFormSet = inlineformset_factory(Receta, Ingrediente, extra=0, can_delete=True)
    InstruccionFormSet = inlineformset_factory(Receta, Instruccion, extra=0, can_delete=True)

    if request.method == 'POST':
        form = RecetaForm(request.POST, instance=receta)
        ingredienteFormset = IngredienteFormSet(request.POST, instance=receta)
        instruccionFormset = InstruccionFormSet(request.POST, instance=receta)

        if form.is_valid() and ingredienteFormset.is_valid() and instruccionFormset.is_valid():
            form.save()
            ingredienteFormset.save()
            instruccionFormset.save()
            return redirect('lista')
    else:
        form = RecetaForm(instance=receta)
        ingredienteFormset = IngredienteFormSet(instance=receta)
        instruccionFormset = InstruccionFormSet(instance=receta)

    return render('registro-edicion.html', locals(),
        context_instance=ctx(request))

~~~


#### 5. TEMPLATES

Necesitamos un template para el listado de recetas:

~~~
::jinja
{% extends 'base.html' %}

{% block body %}
<h1>Recetas</h1>

<ol>
    {% for receta in recetas %}
        <li>
            <a href="{{ receta.get_absolute_url }}">{{ receta.titulo }}</a>
        </li>
    {% endfor %}
</ol>

<a href="{% url 'registrar' %}">Registrar receta</a>
{% endblock body %}
~~~

Observen que hemos añadido un método `get_absolute_url` al modelo `Receta`:

~~~
::python
    def get_absolute_url(self):
        return reverse('editar', kwargs={'receta_id': self.id})
~~~

Y el template para la parte del registro/edición que consta de:

- Sección de administración para los formset (por ejemplo un campo lleva la cuenta del número actual de inlines y otro el del número inicial de los mismos)
- El formulario de la receta
- Los formularios para cada formset
- Un template para cada formset que se toma como base para el proceso de "Añadir un nuevo Ingrediente o Instrucción". Nótese que para clonar este template estoy utilizando un poco de jquery.
- Código javascript que maneja el proceso de clonación

El template es el que sigue:

~~~
::jinja
{% extends 'base.html' %}

{% block body %}
<form method="post" action="#">
    {% csrf_token %}

    {{ IngredienteFormSet.management_form }}
    {{ InstruccionFormSet.management_form }}

    <fieldset class="form ">
        {% for field in form %}
            <div class="form-row">
                <div class="field-box">
                    {{ field.errors }}
                    {{ field.label_tag }}: {{ field }}
                </div>
            </div>
        {% endfor %}
    </fieldset>

    <fieldset>
        <legend>Ingredientes</legend>
        <ul id='formset-ingredientes'>
            {% for form in ingredienteFormset %}
                {{ form.id }}
                <li>
                    {{ form.as_ul }}
                </li>
            {% endfor %}
        </ul>

        <button id='btnIngrediente'>Añadir Ingrediente</button>
    </fieldset>

    <fieldset>
        <legend>Instrucciones</legend>
        <ul id='formset-instrucciones'>
            {% for form in instruccionFormset %}
                {{ form.id }}
                <li>
                    {{ form.as_ul }}
                </li>
            {% endfor %}
        </ul>

        <button id='btnInstruccion'>Añadir Instrucción</button>
    </fieldset>

    <button>Enviar</button>
</form>

<script type='template/ingrediente'>
    {{ ingredienteFormset.empty_form.as_ul }}
</script>

<script type='template/instruccion'>
    {{ instruccionFormset.empty_form.as_ul }}
</script>

<script>
$(function(){

    // Reemplaza todas las coincidencias en vez de solo la primera
    function replaceAll(text, busca, reemplaza){
          while (text.toString().indexOf(busca) != -1)
            text = text.toString().replace(busca, reemplaza);
          return text;
    }

    var $totalIngredientes = $('#id_ingrediente_set-TOTAL_FORMS');

    $('#btnIngrediente').click(function(event) {
        event.preventDefault();
        var total = parseInt($totalIngredientes.val(), 10);
        var clon = $('script[type="template/ingrediente"]').html();
        clon_html = replaceAll(clon, '__prefix__', (total).toString());
        $('#formset-ingredientes').append(clon_html);
        $totalIngredientes.val(total +  1);
    });

    var $totalInstrucciones = $('#id_instruccion_set-TOTAL_FORMS');

    $('#btnInstruccion').click(function(event) {
        event.preventDefault();
        var total = parseInt($totalInstrucciones.val(), 10);
        var clon = $('script[type="template/instruccion"]').html();
        clon_html = replaceAll(clon, '__prefix__', (total).toString());
        $('#formset-instrucciones').append(clon_html);
        $totalInstrucciones.val(total +  1);
    });
})
</script>
{% endblock body %}
~~~

<br>
Y con ello concluye el proceso.. claro, sin olvidar que hay que ensamblar las partes[^3].

Por cierto, si bien he utilizado [vistas basadas en funciones][django-views], sé que es posible realizar lo mismo con las [vistas basadas en clases][django-cbv].

&#42; Aunque tengo mis dudas respecto la complejidad del código en ese otro caso.

- - -

##### Referencias

- [Form with one Formset example][django-form-formset]

[^1]: La idea la tomé de este [post][django-class-based-views-multiple-inline-formsets].

[^2]: En el admin de django es posible editar un modelo con sus "[inline models][django-admin-inline]" mediante los `TabularInline` y `StackedInline`.

[^3]: pero aquello queda de tarea

[django-form-formset]: https://djangosnippets.org/snippets/1246/
[django-class-based-views-multiple-inline-formsets]: http://kevindias.com/writing/django-class-based-views-multiple-inline-formsets/
[django-admin-inline]: https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#django.contrib.admin.TabularInline
[django-inlineformset]: https://docs.djangoproject.com/en/1.7/topics/forms/modelforms/#inline-formsets
[django-views]: https://docs.djangoproject.com/en/1.7/topics/http/views/
[django-cbv]: https://docs.djangoproject.com/en/1.7/topics/class-based-views/