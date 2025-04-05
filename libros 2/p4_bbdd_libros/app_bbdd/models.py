from django.db import models

class Biblioteca(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    biblioteca = models.ForeignKey('Biblioteca', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    editorial = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    fecha_publicacion = models.DateField()
    fecha_adquisicion = models.DateField()
    genero = models.CharField(max_length=100)
    descripcion = models.TextField()
    disponible = models.BooleanField(default=True)  # Campo para indicar si el libro está disponible

    def __str__(self):
        return self.titulo

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=9)
    email = models.EmailField()
    telefono = models.CharField(max_length=9)
    direccion = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return self.nombre


class Prestamos(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField()
    fecha_devolucion = models.DateTimeField(null=True, blank=True)  # Permitir NULL y vacío

    def __str__(self):
        return f"{self.usuario}, {self.libro} : {self.fecha_prestamo} - {self.fecha_devolucion or 'No devuelto'}"