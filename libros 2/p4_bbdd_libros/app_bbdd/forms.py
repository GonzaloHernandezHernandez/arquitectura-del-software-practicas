from django import forms
from .models import Biblioteca,Usuario,Prestamos,Libro

class BibliotecaForm(forms.ModelForm):
    class Meta:
        model = Biblioteca
        fields = '__all__'

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

class PrestamosForm(forms.ModelForm):
    class Meta:
        model = Prestamos
        fields = '__all__'

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'