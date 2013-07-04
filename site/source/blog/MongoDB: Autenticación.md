Title: MongoDB: Autenticación y Autorización
Date: 2013-06-02
Tags: mongodb
Slug: mongodb-autenticacion-autorizacion
Author: __alexander__

Una de las buenas prácticas en cuanto al aspecto de la seguridad en [mongodb][mongodb] corresponde al requerir autenticación para poder acceder a sus instancias.

MongoDB provee soporte para el manejo de autenticación (uso de credenciales de acceso) y autorización (uso de roles).

Podemos activar la autenticación de dos maneras:

1. Creando un usuario administrador y luego activamos la autenticación.

2. Activando la autenticación y creando un administrador

A más detalle:

##### Creando un usuario administrador y luego activamos la autenticación

1. Iniciamos **mongod**[^1] (por defecto la autorización está desactivada)

2. Accedemos a la interfaz interactiva ([mongo][mongo])

        MongoDB shell version: 2.4.3
        connecting to: test
        >

3. Cambiamos la base de datos de test a la de administración:

        > use admin
        switched to db admin


4. Creamos un usuario administrador (aquel que cuenta con uno de los dos siguientes roles: *userAdmin* o *userAdminAnyDatabase*)

        > db.addUser({user:"admin", pwd: "admin", roles: ["userAdminAnyDatabase"]}
        ... )
        {
                "user" : "admin",
                "pwd" : "7c67ef13bbd4cae106d959320af3f704",
                "roles" : [
                        "userAdminAnyDatabase"
                ],
                "_id" : ObjectId("51ac0cca34cad99e8cff6092")
        }

5. Con lo anterior, podemos reiniciar *mongod* con la autenticación activada:

        mongod --auth

A modo de ejemplo, supongamos que disponemos de la base de datos Hospital y deseamos añadir un objeto a la colección pacientes (considerando que hemos activado la autenticación):

        > use Hospital
        switched to db Hospital
        > db.pacientes.insert({"nombre": "alexander", "edad": 23})
        not authorized for insert on Hospital.pacientes

Observamos que no disponemos permisos, asi que primero nos loguearemos en admin, cambiaremos a la bbdd Hospital y crearemos un nuevo usuario para esta otra bbdd:

        > use admin
        switched to db admin
        > db.auth("admin", "admin")
        1
        > use Hospital
        switched to db Hospital
        > db.addUser("doctor", "doctor")
        {
            "user" : "doctor",
            "readOnly" : false,
            "pwd" : "f830c9f104077d9b115e22fd26269824",
            "_id" : ObjectId("51ac13b73d47965438d38b65")
        }
        > db.auth("doctor", "doctor")
        1

Por defecto este usuario tiene permisos de escritura, como observamos aquí:

        > db.pacientes.insert({"nombre": "alexander", "edad": 23})
        > db.pacientes.find()
        { "_id" : ObjectId("51ac13cd3d47965438d38b66"), "nombre" : "alexander", "edad" : 23 }

- - -

Note que para añadir usuarios con roles específicos, debemos usar la sintaxis:

        > db.addUser( { user: "<username>", pwd: "<password>",
        ... roles: [ "rol1", "rol2" ] } )

En donde los roles pueden ser: read, readWrite, dbAdmin, userAdmin.. entre otros. Para más información consulte la [documentación][docs-roles]

- - -

¿Y el segundo método?

El segundo método se aprovecha de la [excepción localhost][localhost-exception]: Si no existen usuarios para la base de datos de *admin*, podemos conectarnos con permisos completos por medio de la interfaz en localhost.

Y una vez accedido al sistema, los pasos para crear usuarios son los que ya se mostraron antes.

[^1]: [mongod][mongod] es el proceso demonio primario de mongodb, controla las solicitudes de datos, administra formatos de datos y realiza varias tareas de administración.

[mongodb]: http://mongodb.org/
[mongod]: http://docs.mongodb.org/manual/reference/program/mongod/
[mongo]: http://docs.mongodb.org/manual/reference/program/mongo/
[docs-roles]: http://docs.mongodb.org/manual/reference/user-privileges/
[localhost-exception]: http://docs.mongodb.org/manual/tutorial/add-user-administrator/#authenticate-with-full-administrative-access-via-localhost