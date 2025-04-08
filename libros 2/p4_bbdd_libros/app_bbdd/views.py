from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Biblioteca,Libro,Usuario,Prestamos
from django.http import JsonResponse
from .forms import BibliotecaForm,UsuarioForm,LibroForm
from django.shortcuts import render, redirect
from django.utils import timezone

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
    bibliotecas = Biblioteca.objects.all()  
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

    elif request.method == 'POST':  
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':  
            try:
                libro = Libro.objects.get(id=id)
                libro.titulo = request.POST.get('titulo', libro.titulo)
                libro.autor = request.POST.get('autor', libro.autor)
                libro.editorial = request.POST.get('editorial', libro.editorial)
                libro.isbn = request.POST.get('isbn', libro.isbn)
                fecha_publicacion = request.POST.get('fecha_publicacion')
                if fecha_publicacion:
                    libro.fecha_publicacion = fecha_publicacion

                fecha_adquisicion = request.POST.get('fecha_adquisicion')
                if fecha_adquisicion:
                    libro.fecha_adquisicion = fecha_adquisicion
                    libro.genero = request.POST.get('genero', libro.genero)
                libro.descripcion = request.POST.get('descripcion', libro.descripcion)
                libro.disponible = request.POST.get('disponible', libro.disponible)
                libro.save()
                return render(request, 'books/editarLibro.html', {'libro': libro, 'mensaje': 'Libro actualizado con éxito'})
                 
            except Libro.DoesNotExist:
                return JsonResponse({"error": "Libro no encontrado"}, status=404)

        elif method == 'DELETE': 
            try:
                libro = Libro.objects.get(id=id)
                libro.delete()
                return redirect('biblioteca_listado')
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
    usuarios = Usuario.objects.all() 
    return render(request, 'users/listado.html', {
        'titulo': 'Listado de Usuario',
        'usuario': usuarios
    })

@csrf_exempt
def UsuariosDetalles(request,id):
   if request.method == 'GET':
        try:
            usuario = Usuario.objects.values("id", "nombre", "apellidos", "dni", "email", "telefono", "direccion", "fecha_nacimiento").get(id=id)

            prestamos = Prestamos.objects.filter(usuario_id=id).all()

            prestamos_list = list(prestamos)
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
        usuario_id = request.POST.get('usuario_id')
        libro_id = request.POST.get('libro_id')

        libro = Libro.objects.get(id=libro_id)

        if not libro.disponible:
            return render(request, 'prestamos/error.html', {
                'mensaje': 'Este libro no está disponible para préstamo.'
            })

        Prestamos.objects.create(
            usuario_id=usuario_id,
            libro=libro,
            fecha_prestamo=timezone.now()
        )

        libro.disponible = False
        libro.save()

        return redirect('prestamolist')

    usuarios = Usuario.objects.all()
    libros_disponibles = Libro.objects.filter(disponible=True)
    return render(request, 'loans/formulario.html', {
        'usuarios': usuarios,
        'libros': libros_disponibles
    })

def prestamo_listado(request):
    loan = Prestamos.objects.all()  
    return render(request, 'loans/listado.html', {
        'titulo': 'Listado de Usuario',
        'loans': loan
    })

@csrf_exempt
def prestamosDeUsuario(request, id):
    if request.method == 'GET':
        prestamos = list(Prestamos.objects.filter(usuario_id=id).values(
            "id", "libro__titulo", "fecha_prestamo", "fecha_devolucion"
        ))
        return JsonResponse(prestamos, safe=False)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def Modificarprestamos(request, id):
    try:
        prestamo = Prestamos.objects.get(id=id)
    except Prestamos.DoesNotExist:
        return JsonResponse({"error": "Préstamo no encontrado"}, status=404)

    if request.method == 'GET':
        return render(request, 'loans/editar.html', {'prestamo': prestamo})

    elif request.method == 'POST':
        fecha_prestamo = request.POST.get('fecha_prestamo')
        fecha_devolucion = request.POST.get('fecha_devolucion')

        if not fecha_prestamo or not fecha_devolucion:
            return render(request, 'loans/editar.html', {
                'prestamo': prestamo,
                'error': 'Todos los campos son obligatorios.'
            })

        prestamo.fecha_prestamo = fecha_prestamo
        prestamo.fecha_devolucion = fecha_devolucion
        prestamo.save()

        libro = prestamo.libro
        libro.disponible = True
        libro.save()

        return render(request, 'loans/editar.html', {
            'prestamo': prestamo,
            'mensaje': 'Préstamo modificado con éxito. El libro ha sido devuelto y está disponible.'
        })

    return JsonResponse({"error": "Método no permitido"}, status=405)