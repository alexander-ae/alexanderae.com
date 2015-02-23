Title: Acceso SSH sin password
Date: 2013-03-24 12:00
Tags: linux, sysadmin,
Slug: acceso-ssh-sin-password
Author: __alexander__

Introducir una contraseña cada vez que necesitamos iniciar una conexión [**ssh**][ssh] con el servidor, puede ser algo incómodo[^1].

Afortunadamente, revisando sobre ello, encontré que es posible acceder mediante un método alternativo: llaves ssh[^2].

- - -

Para ello, supongamos que tenemos 2 pc's a las que llamaremos *A* y *B*, con los usuarios *a* y *b* respectivamente.

Lo que se desea es poder acceder desde la pc A hacia B con el usuario b. Para lo cual seguiremos los siguientes pasos:

1. En la pc 'A' generamos una llave pública y privada sin la frase de contraseña.

        a@A:~> ssh-keygen -t rsa
        Generating public/private rsa key pair.
        Enter file in which to save the key (/home/a/.ssh/id_rsa):
        Created directory '/home/a/.ssh'.
        Enter passphrase (empty for no passphrase):
        Enter same passphrase again:
        Your identification has been saved in /home/a/.ssh/id_rsa.
        Your public key has been saved in /home/a/.ssh/id_rsa.pub.
        The key fingerprint is:
        1a:2b:3c:4d:5e:6f:77:8h:9i:jj:k0:1a:2b:3c:4d:5e a@A


2. Creamos el directorio *~/.ssh* en *B*, considerando que puede ya existir:

        a@A:~> ssh b@B mkdir -p .ssh
        b@B's password:

3. Añadimos nuestra llave pública creada en *A* al archivo *ssh/authorized_keys* en *B*:

        a@A:~> cat .ssh/id_rsa.pub | ssh b@B 'cat >> .ssh/authorized_keys'
        b@B's password:

##### Nota:

Es posible que necesitemos ajustar los permisos del directorio *.ssh* y el archivo *.ssh/authorized_keys*.

    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/authorized_key


Una vez listo lo anterior,podríamos acceder por ssh al servidor B sin necesidad de escribir nuestra contraseña.

- - -

##### Actualización

Un método mucho más simple para copiar nuestra clave ssh al servidor al que accederemos es mediante el comando *ssh-copy-id*:

        ssh-copy-id -i .ssh/id_rsa.pub user@host

Lo cual resulta mucho más veloz que el método anterior.

- - -

##### Referencias

1. SSH login without password: [linuxproblem.org][linuxproblem.org]

2. ssh - authorized_keys HOWTO: [universidad de cambridge][universidad-de-cambridge]

3. Acceso a máquinas usando ssh sin contraseña: [universidad de valencia][universidad-de-valencia]

[^1]: en especial cuando la contraseña es una larga cadena de caracteres inmemorizables y son varios los servidores con los que se trabaja.

[^2]: [ssh keys][ssh-keys]


[ssh]: http://es.wikipedia.org/wiki/Secure_Shell
[ssh-keys]: https://wiki.archlinux.org/index.php/SSH_Keys
[linuxproblem.org]: http://linuxproblem.org/art_9.html
[universidad-de-cambridge]: http://www.eng.cam.ac.uk/help/jpmg/ssh/authorized_keys_howto.html
[universidad-de-valencia]: http://www.uv.es/~sto/articulos/BEI-2003-01/ssh_np.html