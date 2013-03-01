Title: Limpiar o resetear formularios en JS
Date: 2013-02-28
Tags: js
Slug: clear-reset-form-js
Author: __alexander__

Fragmentos de código para limpiar o resetear formularios en JS. Note que "limpiar" borrará todo el contenido del formulario mientras que "resetear" restaurará los valores iniciales.

####Reset form

Para resetear formularios existe un [método][reset-form] de los forms:

~~~~
::javascript
document.getElementById("test-form").reset();
~~~~

####Clear form
Para limpiar formularios en cambio, tenemos que escribir nuestra propia función, como por ejemplo[^1]:

~~~~
::javascript
function clearForm(oForm) {

  var elements = oForm.elements; 

  oForm.reset();

  for(i=0; i<elements.length; i++) {
      
    field_type = elements[i].type.toLowerCase();

    switch(field_type) {
      case "text":
      case "email":
      case "password":
      case "textarea":
      case "hidden":
        elements[i].value = ""; 
        break;

      case "radio":
      case "checkbox":
          if (elements[i].checked) {
            elements[i].checked = false;
        }
        break;

      case "select-one":
      case "select-multi":
        elements[i].selectedIndex = -1;
        break;

      default:
        break;
    }
  }
}
~~~~

y la llamamos mediante:

~~~~
::javascript
clearForm(form);
~~~~

#### demo
A modo de ejemplo, puede visitar el siguiente [link][demo].

El código se puede visualizar en el directorio 'clear-reset-form' del [repo][repo-demo]


[^1]: Visto en: [javascript-coder.com]

[reset-form]: http://www.w3schools.com/jsref/met_form_reset.asp
[javascript-coder.com]: http://www.javascript-coder.com/javascript-form/javascript-reset-form.phtml
[repo-demo]: https://bitbucket.org/__alexander__/alexander-ae-site-static-demos
[demo]: http://labs.alexanderae.com/clear-reset-form/