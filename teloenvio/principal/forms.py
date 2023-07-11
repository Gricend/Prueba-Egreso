import random
import string
from django import forms
from django.core.mail import send_mail
from principal.models import Cliente, Producto
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    usuario = forms.CharField(label='Usuario')
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class RegistroClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('fono', 'correo', 'nombre', 'numIdentificador', 'direccion', 'comuna')

    def save(self, commit=True):
        cliente = super().save(commit=False)
        username = self.cleaned_data['nombre']
        password = self._generate_random_password()
        user = User.objects.create_user(username=username, password=password)
        cliente.user = user
        if commit:
            cliente.save()
            self._send_confirmation_email(cliente.correo, password)
        return cliente

    def _generate_random_password(self):
        length = 6
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def _send_confirmation_email(self, email, password):
        subject = 'Confirmación de registro'
        message = f'Su registro ha sido exitoso. Su contraseña para ingresar a sus pedidos es: {password}'
        from_email = 'noreply@example.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

class CrearProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('idProductor', 'descripcionProducto', 'precioProducto', 'imagenProducto', 'stockProducto')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagenProducto'].required = False 

    def clean_precioProducto(self):
        precio = self.cleaned_data.get('precioProducto')
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor que cero.')
        return precio

    def clean_stockProducto(self):
        stock = self.cleaned_data.get('stockProducto')
        if stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock