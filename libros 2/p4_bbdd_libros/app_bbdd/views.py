from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Biblioteca,Libro,Usuario,Prestamos
import json
from django.http import JsonResponse,HttpResponseRedirect
from .forms import BibliotecaForm,UsuarioForm,PrestamosForm,LibroForm
from django.shortcuts import render, redirect


# Create your views here.
@csrf_exempt
def biblioteca(request):
    if request.method == 'POST':
        form = BibliotecaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('biblioteca_listado')  
        return JsonResponse({"error": "Datos incompletos o inválidos"}, status=400)

    bibliotecas = Biblioteca.objects.all()  

    form = BibliotecaForm()
    return render(request, 'libraries/formulario.html', {
        'form': form, 
        'titulo': 'Listado de bibliotecas',
        'bibliotecas': bibliotecas
    })

def biblioteca_listado(request):
    bibliotecas = Biblioteca.objects.all()  # Obtener el listado de bibliotecas
    return render(request, 'libraries/listado.html', {
        'titulo': 'Listado de bibliotecas',
        'bibliotecas': bibliotecas
    })

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
        form = LibroForm(request.POST)
        if form.is_valid():
            nuevo_libro = form.save() 
            return redirect('detalles_libro', id=nuevo_libro.id)  
    else:
        form = LibroForm()

    return render(request, 'books/nuevoLibro.html', {'form': form, 'titulo': 'Agregar Nuevo Libro'})


@csrf_exempt
def librosEnBiblioteca(request,id):     
    if request.method == 'GET':
        libros = list(Libro.objects.filter(biblioteca_id=id))

        return render(request, 'libraries/librosEnBiblioteca.html', {
        'titulo': 'Listado de libros',
        'id': id,
        'libros': libros})

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def detallesOeditarOeliminar_libros(request, id):
    if request.method == 'GET':  
        try:
            libro = Libro.objects.get(id=id)
            return render(request, 'books/detallesLibro.html', {'libro': libro})
        except Libro.DoesNotExist:
            return JsonResponse({"error": "Libro no encontrado"}, status=404)

    elif request.method == 'POST':  # Para manejar PUT o DELETE desde un formulario
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':  # Editar libro
            try:
                libro = Libro.objects.get(id=id)
                libro.titulo = request.POST.get('titulo', libro.titulo)
                libro.autor = request.POST.get('autor', libro.autor)
                libro.editorial = request.POST.get('editorial', libro.editorial)
                libro.isbn = request.POST.get('isbn', libro.isbn)
                libro.fecha_publicacion = request.POST.get('fecha_publicacion', libro.fecha_publicacion)
                libro.fecha_adquisicion = request.POST.get('fecha_adquisicion', libro.fecha_adquisicion)
                libro.genero = request.POST.get('genero', libro.genero)
                libro.descripcion = request.POST.get('descripcion', libro.descripcion)
                libro.disponible = request.POST.get('disponible', libro.disponible)
                libro.save()
                return render(request, 'books/editarLibro.html', {'libro': libro, 'mensaje': 'Libro actualizado con éxito'})
                 
            except Libro.DoesNotExist:
                return JsonResponse({"error": "Libro no encontrado"}, status=404)

        elif method == 'DELETE':  # Eliminar libro
            try:
                libro = Libro.objects.get(id=id)
                libro.delete()
                return redirect('detalles_libro', id=libro.id)
            except Libro.DoesNotExist:
                return JsonResponse({"error": "Libro no encontrado"}, status=404)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def crearUsuarios(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios_listado')  
        return JsonResponse({"error": "Datos incompletos o inválidos"}, status=400)

    Usuarios = Usuario.objects.all()  

    form = UsuarioForm()
    return render(request, 'users/formulario.html', {
        'form': form, 
        'titulo': 'Listado de Ususarios',
        'usuario': Usuarios
    })

def usuarios_listado(request):
    usuarios = Usuario.objects.all()  # Obtener el listado de bibliotecas
    return render(request, 'users/listado.html', {
        'titulo': 'Listado de Usuario',
        'usuario': usuarios
    })

@csrf_exempt
def UsuariosDetalles(request,id):
   if request.method == 'GET':
        try:
            # Obtener los detalles del usuario
            usuario = Usuario.objects.values("id", "nombre", "apellidos", "dni", "email", "telefono", "direccion", "fecha_nacimiento").get(id=id)

            # Obtener los préstamos del usuario
            prestamos = Prestamos.objects.filter(usuario_id=id).values(
                "libro__titulo", 
                "libro__autor", 
                "libro__isbn", 
                "fecha_prestamo", 
                "fecha_devolucion"
            )

            # Convertir los préstamos a una lista
            prestamos_list = list(prestamos)

            # Devolver los detalles del usuario junto con sus préstamos
            response_data = {
                "usuario": usuario,
                "prestamos": prestamos_list
            }

            return render(request, 'users/detalles_usuario.html', {
            'usuario': usuario,
            'prestamos': prestamos,
        })
        except Usuario.DoesNotExist:
            return render(request, 'usuarios/error.html', {'message': 'Usuario no encontrado'})

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