Title: Vue + Summernote Editor
Date: 2020-07-27
Tags: vuejs, javascript
Slug: vue-summernote-editor
Author: __alexander__
Summary: Ejemplo mínimo que muestra cómo integrar vue.js y summernote editor. 

Parte de un desarrollo que estoy realizando requiere integrar <a href="https://vuejs.org/" target="_blank">Vue.js</a> y <a href="https://summernote.org/" target="_blank">Summernote</a>. Lamentablemente no existe una integración oficial por lo que anotaré los pasos que seguí por si le son de ayuda a alguien.

1. Observemos que yo ya tengo un proyecto creado con **vue-cli**
2. Instalo las dependencias necesarias

    - yarn add jquery
    - yarn add summernote
    
3. Creo un componente al que llamaré *Summernote.vue*, con un contenido similar a:

~~~
::javascript
<template>
    <div :id="element">
        <slot></slot>
    </div>
</template>

<script>
    const $ = require("jquery")
    import "summernote/dist/summernote-lite.min.css";
    import "summernote/dist/summernote-lite.min";

    export default {
        name: "Summernote",
        data() {
            return {
                element: `summernote_${new Date().getTime()}`
            };
        },
        props: {
            config: {
                type: Object
            },
            ready: {
                type: Function
            }
        },
        mounted() {
            this.$nextTick(() => {
                let defaultConfig = {
                    //lang: "es-ES",
                    placeholder: "placeholder...",
                    height: 600,
                    width: 810,
                    focus: true,
                    callbacks: {
                        onInit: () => {
                            this.$emit("ready", this);
                        },
                        onChange: contents => {
                            this.$emit("change", contents);
                        },
                        onEnter: () => {
                            this.$emit("enter");
                        },
                        onFocus: () => {
                            this.$emit("focus");
                        },
                        onBlur: () => {
                            this.$emit("blur");
                        },
                        onKeyup: e => {
                            this.$emit("keyup", e);
                        },
                        onKeydown: e => {
                            this.$emit("keydown", e);
                        },
                        onPaste: e => {
                            this.$emit("paste", e);
                        },
                    }
                };
                let config = Object.assign({}, defaultConfig, this.config);
                $("#" + this.element).summernote(config);
            });
        },
        methods: {
            summernote(...args) {
                $("#" + this.element).summernote(...args);
            },
            ui() {
                return $.summernote.ui;
            }
        }
    };
</script>
<style scoped>
    .summernote-img {
        max-width: 100%;
    }
</style>
~~~

Noten que estoy usando la versión lite de **summernote**, aquella que no requiere bootstrap.

Ahora, con lo anterior, puedo utilizar mi componente recién creado, por ejemplo:

~~~
::html
<template>
    <div>
        <summernote :config="summernoteConfig" @ready="readySummernote"></summernote>
    </div>
    <div class="preview">
        <div v-html="contents"></div>
    </div>
</template>

<script>
    import Summernote from "../Summernote";

    export default {
        name: "AnotherComponent",
        components: {
            Summernote
        },
        data() {
            return {
                summernoteConfig: {
                    placeholder: '',
                    tabsize: 2,
                    height: 200,
                    toolbar: [
                        ['font', ['bold', 'underline', 'clear']],
                        ['font', ['superscript', 'subscript']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['table', ['table']],
                        ['insert', ['picture', 'hr']],
                        ['view', ['codeview']],
                    ]
                },
                contents: ""
            }
        },
        methods: {
            readySummernote(editor) {
                editor.summernote('code', this.contents);
                editor.$on("change", contents => {
                    this.contents = contents;
                });
            }
        }
    }
</script>
~~~ 

Lo que hicimos fue:
 
 1. Importar el componente que creamos para "Summernote"
 2. Crear una variable para la configuración del editor
 3. Creamos un método que reciba los cambios del contenido y los asigne a una variable que le indicamos.
 4. En el html también hemos incluido una vista previa de lo que genera el editor.
 
 - - -
 
Debido a que mi conocimiento del javascript (vue) no es el suficiente, hay algunos otros puntos que intenté realizar y no pude, como por ejemplo:
 
 - integrar katex (un plugin de summernote para utilizar latex)
 - cambiar el idioma de summernote (tuve conflictos con jquery)
 
Pero espero que al menos como base lo anterior le sea de ayuda a alguien.
 
<br>
##Referencias
 
 - <a href="https://github.com/pasBone/vue-summernote-lite" target="_blank">vue summernote lite</a>: un repositorio del que me guié y a quien pertenece la mayoría de la lógica utilizada aquí
 - <a href="https://github.com/summernote/summernote/issues/2597" target="_blank">How do I use Summernote with the Vue.js Framework?
</a>: un issue en el repositorio de summernote el cual da algunas otras ideas del cómo enfocar el problema

Si les fue de ayuda, compartan la publicación o dejen un comentario :)
<br>