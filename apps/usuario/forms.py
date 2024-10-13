from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingresa una dirección de correo válida.")
    
    class Meta:
        model = Usuario
        fields = ['email', 'dni', 'nombre', 'apellidos', 'celular', 'password1', 'password2']
        labels = {
            'email': 'Correo electrónico',
            'dni': 'DNI',
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'celular': 'Celular'
        }
        help_texts = {
            'dni': 'Ingrese su DNI de 8 dígitos.',
            'celular': 'Ingrese su número de celular de 9 dígitos.'
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email
    
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Usuario.objects.filter(dni=dni).exists():
            raise forms.ValidationError("Este DNI ya está registrado.")
        return dni
    
    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if Usuario.objects.filter(celular=celular).exists():
            raise forms.ValidationError("Este número de celular ya está registrado.")
        return celular
