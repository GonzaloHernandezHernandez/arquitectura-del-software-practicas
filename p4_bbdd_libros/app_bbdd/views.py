from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Biblioteca,Libro,Usuario,Prestamos
import json
from django.http import JsonResponse

# Create your views here.
@csrf_exempt
def biblioteca(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Biblioteca.objects.create(
                nombre = data.get('nombre'),
                direccion = data.get('direccion'),
                telefono = data.get('telefono'),
                email = data.get('email')
            )
            return JsonResponse({"mensaje": "Biblioteca registrado con éxito" }, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
        
    if request.method == 'GET':
            bibliotecas = list(Biblioteca.objects.values("nombre"))

            return JsonResponse(bibliotecas, safe=False)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def bibliotecaById(request,id):
    if request.method == 'GET':
        try:
            biblioteca = Biblioteca.objects.values("nombre", "direccion", "telefono", "email").get(id=id)
            return JsonResponse(biblioteca)
        except Biblioteca.DoesNotExist:
            return JsonResponse({"error": "Biblioteca no encontrada"}, status=404)
    
@csrf_exempt
def libros(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            biblioteca = Biblioteca.objects.get(id=data.get('biblioteca_id'))
            Libro.objects.create(
                biblioteca = biblioteca,
                titulo = data.get('titulo'),
                autor = data.get('autor'),
                editorial = data.get('editorial'),
                isbn = data.get('isbn'),
                fecha_publicacion = data.get('fecha_publicacion'),
                fecha_adquisicion = data.get('fecha_adquisicion'),
                genero = data.get('genero'),
                descripcion = data.get('descripcion'),
            )
            return JsonResponse({"mensaje": "Libro registrado con éxito" }, status=404)
        except Libro.DoesNotExist:
            return JsonResponse({"error": "Libro no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)


@csrf_exempt
def librosEnBiblioteca(request,id):     
    if request.method == 'GET':
        libros = list(Libro.objects.values("titulo").filter(biblioteca_id=id))

        return JsonResponse(libros, safe=False)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def detallesOeditarOeliminar_libros(request,id):
    if request.method == 'GET':
        try:
            libro = Libro.objects.values("titulo", "autor", "editorial", "isbn", "fecha_publicacion", "fecha_adquisicion", "genero", "descripcion").get(id=id)
            return JsonResponse(libro)
        except Libro.DoesNotExist:
            return JsonResponse({"error": "Libro no encontrado"}, status=404)
    
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            libro = Libro.objects.get(id=id)
            libro.titulo = data.get('titulo')
            libro.autor = data.get('autor')
            libro.editorial = data.get('editorial')
            libro.isbn = data.get('isbn')
            libro.fecha_publicacion = data.get('fecha_publicacion')
            libro.fecha_adquisicion = data.get('fecha_adquisicion')
            libro.genero = data.get('genero')
            libro.descripcion = data.get('descripcion')
            libro.save()
            return JsonResponse({"mensaje": "Libro modificado con éxito" }, status=404)
        except Libro.DoesNotExist:
            return JsonResponse({"error": "Libro no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    if request.method == 'DELETE':
        try:
            libro = Libro.objects.get(id=id)
            libro.delete()
            return JsonResponse({"mensaje": "Libro eliminado con éxito" }, status=404)
        except Libro.DoesNotExist:
            return JsonResponse({"error": "Libro no encontrado"}, status=404)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def crearOlistarUsuarios(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Usuario.objects.create(
                nombre = data.get('nombre'),
                apellidos = data.get('apellidos'),
                dni = data.get('dni'),
                email = data.get('email'),
                telefono = data.get('telefono'),
                direccion = data.get('direccion'),
                fecha_nacimiento = data.get('fecha_nacimiento')
            )
            return JsonResponse({"mensaje": "Usuario registrado con éxito" }, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
        
    if request.method == 'GET':
            usuarios = list(Usuario.objects.values("nombre", "apellidos"))

            return JsonResponse(usuarios, safe=False)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def UsuariosDetalles(request,id):
    if request.method == 'GET':
        try:
            usuario = Usuario.objects.values("nombre", "apellidos", "dni", "email", "telefono", "direccion", "fecha_nacimiento").get(id=id)
            return JsonResponse(usuario)
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def prestamos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            usuario = Usuario.objects.get(id=data.get('usuario_id'))
            libro = Libro.objects.get(id=data.get('libro_id'))
            Prestamos.objects.create(
                usuario = usuario,
                libro = libro,
                fecha_prestamo = data.get('fecha_prestamo'),
                fecha_devolucion = data.get('fecha_devolucion')
            )
            return JsonResponse({"mensaje": "Prestamo registrado con éxito" }, status=404)
        except Prestamos.DoesNotExist:
            return JsonResponse({"error": "Prestamo no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    if request.method == 'GET':
        prestamos = list(Prestamos.objects.values("usuario", "libro", "fecha_prestamo", "fecha_devolucion"))
        return JsonResponse(prestamos, safe=False)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def prestamosDeUsuario(request,id):
    if request.method == 'GET':
        prestamos = list(Prestamos.objects.values("usuario", "libro", "fecha_prestamo", "fecha_devolucion").filter(usuario_id=id))
        return JsonResponse(prestamos, safe=False)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def Modificarprestamos(request,id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            prestamo = Prestamos.objects.get(id=id)
            prestamo.fecha_prestamo = data.get('fecha_prestamo')
            prestamo.fecha_devolucion = data.get('fecha_devolucion')
            prestamo.save()
            return JsonResponse({"mensaje": "Prestamo modificado con éxito" }, status=404)
        except Prestamos.DoesNotExist:
            return JsonResponse({"error": "Prestamo no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)