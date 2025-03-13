# arquitectura-del-software-practicas
En este repositorio Gonzalo Hernández guardara todas las prácticas de clase evaluables

las rutas de acceso para las llamadas son

BIBLIOTECA
POST y GET
http://127.0.0.1:8000/libraries/
GET by id
http://127.0.0.1:8000/libraries/<int:id>/

LIBROS
POST 
http://127.0.0.1:8000/books/
GET (listado libros de una biblioteca)
http://127.0.0.1:8000/libraries/<int:id>/books/
GET (detalles del libro) , PUT, DELETE ( por id )
http://127.0.0.1:8000/books/<int:id>/

USUARIOS
POST y GET 
http://127.0.0.1:8000/users/
GET (detalles usuario)
http://127.0.0.1:8000/users/<int:id>/

PRESTAMOS
POST y GET
http://127.0.0.1:8000/loans/
GET (presatamos de un usuario por id)
http://127.0.0.1:8000/users/<int:id>/loans/
PUT (modificar prestamo por id)
http://127.0.0.1:8000/loans/<int:id>/
