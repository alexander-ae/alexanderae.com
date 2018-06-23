Title: Cómo hacer un form field de solo lectura en django
Date: 2018-06-22
Tags: django,
Slug: django-form-field-readonly
Author: __alexander__

Para hacer un *"Form Field"* de solo lectura basta utilizar el atributo "attrs" de los widgets y agregar la propiedad *readonly* como en el siguiente ejemplo:

Antes:    
~~~
::python
from django import forms

class CommentForm(forms.Form):
    name = forms.CharField()
~~~

Después:

~~~
::python
class CommentForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
~~~

### Observación:
Notemos que cuando un input es de solo lectura, el usuario no puede modificarlo pero se sigue enviando en el formulario.

Para desactivar el envío totalmente se puede usar el atributo *disabled* de los *form fields*.

~~~
::python
class CommentForm(forms.Form):
    name = forms.CharField(disabled=True)
~~~

### Referencias:

- [Django docs: customizing widget instances](https://docs.djangoproject.com/en/2.1/ref/forms/widgets/#customizing-widget-instances)
- [Django docs: core field arguments](https://docs.djangoproject.com/en/2.1/ref/forms/fields/#disabled)

<script type="application/ld+json">
{
    "@context": "http://schema.org",
    "@type": "Question",
    "name": "¿Cómo hacer un form field de solo lectura en django?",
    "text": "",
    "dateCreated": "2018-06-22",
    "acceptedAnswer": {
        "@type": "Answer",
        "text": "Para hacer un form field de solo lectura basta utilizar el atributo attrs de los widgets de django como el siguiente ejemplo.",
        "dateCreated": "2018-06-22",
        "author": {
            "@type": "Person",
            "name": "__alexander__"
        }
    }
}
</script>