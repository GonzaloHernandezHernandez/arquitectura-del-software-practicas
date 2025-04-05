from django.urls import path
from django.urls import path
from . import views 


urlpatterns = [
    path('libraries/', views.biblioteca, name='biblioteca'),
    path('libraries/list', views.biblioteca_listado, name='biblioteca_listado'),
    path('libraries/<int:id>/', views.bibliotecaById, name='obtener_bibliotecaid'),
    path('books/', views.libros, name='libro'),
    path('libraries/<int:id>/books/', views.librosEnBiblioteca, name='libro_en_biblioteca'),
    path('books/<int:id>/', views.detallesOeditarOeliminar_libros, name='detalles_libro'),
    path('users/', views.crearUsuarios, name='usuario'),
    path('users/list', views.usuarios_listado, name='usuarios_listado'),
    path('users/<int:id>/', views.UsuariosDetalles, name='usuarioDetalles'),
    path('loans/', views.prestamos, name='prestamo'),
    path('users/<int:id>/loans/', views.prestamosDeUsuario, name='prestamoUsuario'),
    path('loans/<int:id>/', views.Modificarprestamos, name='prestamoModificado'),
    ]