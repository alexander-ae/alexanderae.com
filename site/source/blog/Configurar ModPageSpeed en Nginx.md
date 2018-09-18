Title: Instalar y configurar ModPageSpeed en nginx
Date: 2018-09-18
Tags: nginx, optimizacion
Slug: modpagespeed-nginx
Author: __alexander__

Hoy estuve investigando cómo mejorar el puntage de [Google PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights/?hl=es), el cual es una página de google que mide la velocidad de carga de un website además de brindar algunas recomendaciones para mejorar dichas estadísticas.

Investigando encontré [ModPageSpeeed](https://www.modpagespeed.com/) un módulo para **nginx** (y apache) que realiza varias de aquellas optimizaciones, algunas como:

- Minificar el html
- Unificar archivos css o js
- Convertir formatos de imágenes (como de jpg a webp si el navegador lo soporta)

## Instalación con nginx (ubuntu server)

Activar el módulo requiere que nginx haya sido compilado con ModPageSpeed como extra, esto significa, que en caso ya contemos con nginx, deberemos reinstalarlo.

1. Nos aseguramos que tengamos instaladas las dependencias necesarias por nginx, esta referencia puede ayudarnos: [Install and compile nginx](http://sharadchhetri.com/2018/05/15/install-and-compile-nginx-1-14-on-ubuntu-18-04-lts-server/)

    *Nota:* la referencia es tan solo para las dependencias mas no para el proceso de compilar nginx

    Por ejemplo:
    
        sudo apt-get install gcc lipcre3-dev zlib1g-dev libssl-dev libxml2-dev libxslt1-dev \
            libgd-dev libperl-dev libgd-dev libgeoip1 libgeoip-dev unzip uuid-dev \
            libjpeg-dev libfreetype6 libfreetype6-dev libtiff5-dev libwebp-dev liblcms2-dev \
            libxslt-dev

2. Utilizamos la instalación automática recomendada por ModPageSpeed

        bash <(curl -f -L -sS https://ngxpagespeed.com/install) --nginx-version latest
        
3. Durante el proceso es posible que se nos pregunte si deseamos agregar algun parámetro extra durante la configuración, en mi caso agregué:

        --with-debug --with-pcre-jit --with-http_ssl_module --with-http_stub_status_module --with-http_realip_module --with-http_auth_request_module --with-http_v2_module --with-http_dav_module --with-http_slice_module --with-threads --with-http_addition_module --with-http_geoip_module=dynamic --with-http_gunzip_module --with-http_gzip_static_module --with-http_image_filter_module=dynamic --with-http_sub_module --with-http_xslt_module=dynamic --with-stream=dynamic --with-stream_ssl_module --with-stream_ssl_preread_module
        
    esto por ejemplo para contar con características como [http2](https://www.xataka.com/servicios/http-2-asi-va-a-mejorar-la-velocidad-de-tu-navegacion-sin-que-tu-tengas-que-hacer-nada) o geoip.
    
4. Listo, ya lo tenemos instalado. En mi caso, en el directorio:

        /usr/local/nginx
        
## Configuración

Asumiendo que ya tengamos algún server block ejecutándose:

**1.** Crear un directorio como "/var/ngx_pagespeed_cache" y cambiar el propietario a nuestro usuario de nginx. Aquí se almacenan los archivos temporales que va generar **ModPageSpeed**

**2.** Añadir una configuración similar a la [siguiente](https://gist.github.com/annez/ded1d21999b790612dce) en cada server block donde necesitemos ModPageSpeed:

        pagespeed on;
        pagespeed FileCachePath /var/ngx_pagespeed_cache;
        pagespeed EnableFilters combine_css,extend_cache,rewrite_images,lazyload_images,collapse_whitespace,inline_javascript,inline_css,local_storage_cache,prioritize_critical_css;
        pagespeed EnableFilters rewrite_css,rewrite_javascript;
        # Ensure requests for pagespeed optimized resources go to the pagespeed handler
        # and no extraneous headers get set.
        location ~ "\.pagespeed\.([a-z]\.)?[a-z]{2}\.[^.]{10}\.[^.]+" {
          add_header "" "";
        }
        location ~ "^/pagespeed_static/" { }
        location ~ "^/ngx_pagespeed_beacon$" { }
        
**3.** Noten que podemos activar o desactivar los filtros a utilizar en la directiva *"pagespeed EnableFilters"* según los necesitemos.

**4.** Reiniciamos nginx y eso es todo
    
        ./nginx -s reload

*Nota*: cuando hemos instalado nginx, no se agregó al "path", ni tampoco se creó algun script para que auto-inicie, aquello queda a criterio del usuario.

*Nota 2*: siempre midan el cómo estaba antes y después, de ese modo se compara si realmente hubo alguna mejora o no (en mi caso la hubo).