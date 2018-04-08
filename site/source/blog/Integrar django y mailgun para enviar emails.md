Title: Cómo integrar django y mailgun
Date: 2018-04-08 10:26
Tags: django,
Slug: como-integrar-django-y-mailgun
Author: __alexander__

**Mailgun** es un servicio que permite enviar *emails transaccionales* y emails masivos mediante la integración con su API o via SMTP.

Entre las ventajas de mailgun tenemos:

- permite monitorizar el estado del envío del email: ¿llegó al destino?, ¿fue rechazado?, entre otros.
- permite envíos masivos
- tiene integración con webhooks para eventos como: cuando el recipiente abre el mensaje, abre un enlace, sucede un problema al enviar el email entre otros.
- permite manejar varios dominios de forma separada para que uno no afecte la reputación de los demás en caso de algún problema de spam

### Los pasos para realizar la integración son:

*1.* Registrar una cuenta en [www.mailgun.com](www.mailgun.com) notando que cada mes tendremos para enviar hasta 10 000 emails gratuitos.

![Registro en mailgun][mailgun-registro]

*2.* Luego en la opción *dominios* debemos agregar el dominio que enviará los correos.

![Agregar dominio en mailgun][mailgun-dominio]

Observemos que nos recomiendan usar un subdominio (el detalle se puede revisar en sus preguntas frecuentes).

*3.* Ahora que tenemos un dominio, debemos realizar algunas validaciones y configuraciones. Para esto, requerimos acceso al panel que gestiona los registros DNS del dominio.

La validación requerida es:
![Validación de un dominio en mailgun][mailgun-validar-dominio]

En el caso de digital ocean lo editamos en la sección *"Networking"*:

![Edición de registros DNS en digital ocean][digital-ocean-dns]

*4.* Esperamos un tiempo prudencial (en el caso de digital ocean fueron 3 minutos, pero puede tomar horas según el proveedor) y presionamos el botón para validar los cambios.

![Credenciales de mailgun][mailgun-credenciales]

*5.* El último paso es editar la configuración de envío de correos de django. En nuestro *settings.py* cambiamos los valores a algo como:

~~~
::django
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'postmaster@mailgun.librera.pe'
EMAIL_HOST_PASSWORD = 'not-my-real-password'
DEFAULT_FROM_EMAIL = 'postmaster@mailgun.librera.pe'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
~~~

Y listo, eso es todo, ya podemos enviar correos.

**Nota:** se recomienda que las credenciales esten fuera del archivo settings como en variables de entorno o algún otro método.

En caso se desee integrar características avanzadas de mailgun como 
webhooks, revisen su documentación, allí hay ejemplos de cómo manejarlo.

### Más información

1. [Diferencias entre email marketing vs email transaccional][email-marketing-transaccional]

2. [Documentación de mailgun][mailgun-docs]

3. [How to configure mailgun to send emails in a django app][mailgun-django]

4. [Djando docs: sending email][django-docs]

[email-marketing-transaccional]: https://www.40defiebre.com/diferencias-email-marketing-vs-email-transaccional/
[mailgun-docs]: https://documentation.mailgun.com/en/latest/
[mailgun-django]: https://simpleisbetterthancomplex.com/tutorial/2017/05/27/how-to-configure-mailgun-to-send-emails-in-a-django-app.html
[django-docs]: https://docs.djangoproject.com/en/2.0/topics/email/

[mailgun-registro]: pictures/mailgun-registro.png 'Registro en mailgun'
[mailgun-dominio]: pictures/mailgun-dominio.png 'Dominio en mailgun'
[mailgun-validar-dominio]: pictures/mailgun-validar-dominio.png 'Validación de un dominio en mailgun'
[digital-ocean-dns]: pictures/digital-ocean-dns.png 'Edición de registros DNS en digital ocean'
[mailgun-credenciales]: pictures/mailgun-dominio-validado.png 'Credenciales de mailgun'