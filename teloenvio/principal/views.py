import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from principal.models import Pedido, DetallePedido, Cliente, Producto
from django.contrib.auth.models import User
from .forms import CrearProductoForm, RegistroClienteForm
from django.views.decorators.cache import never_cache
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

# Create your views here.

def home(request):
    return render(request, 'principal/home.html')

@receiver(pre_save, sender=Pedido)
def generar_numero_pedido(sender, instance, **kwargs):
    if not instance.numero_pedido:
        instance.numero_pedido = get_random_string(length=10)

from django.shortcuts import render
from django.views import View

class TomarPedidoView(View):
    def get(self, request):
        productos = Producto.objects.all()
        clientes = Cliente.objects.all()

        context = {
        'productos': productos,
        'clientes': clientes,
        }

        return render(request, 'principal/tomar_pedido.html', context)

    def post(self, request):
        cliente_id = request.POST.get('cliente_id')
        direccion_entrega = request.POST.get('direccion_entrega')
        forma_pago = request.POST.get('forma_pago')
        productos = request.POST.getlist('productos')
        cantidades = request.POST.getlist('cantidades')  

        pedido = Pedido(cliente_id=cliente_id, direccion_entrega=direccion_entrega, forma_pago=forma_pago)
        pedido.save()

        for producto_id, cantidad in zip(productos, cantidades):
            detalle_pedido = DetallePedido(pedido=pedido, producto_id=producto_id, cantidad=cantidad)
            detalle_pedido.save()

        context = {
        'numero_pedido': pedido.numero_pedido,
        'detalle_pedido': detalle_pedido,
        }

        return render(request, 'principal/pedido_confirmado.html', context)

class SeguimientoPedidosView(View):
    def get(self, request):
        pedidos = Pedido.objects.all()
        return render(request, 'principal/seguimiento_pedidos.html', {'pedidos': pedidos})
    
class ActualizarEstadoPedidoView(View):
    def get(self, request, pedido_id):
        pedido = Pedido.objects.get(id=pedido_id)
        return render(request, 'principal/actualizar_estado.html', {'pedido': pedido})

    def post(self, request, pedido_id):
        nuevo_estado = request.POST.get('estado')
        pedido = Pedido.objects.get(id=pedido_id)
        pedido.estado = nuevo_estado
        pedido.save()
        # Lógica para enviar notificación por correo electrónico al cliente
        # ...

        return redirect('seguimiento_pedidos')
    
@never_cache
def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige a la página de inicio después del registro exitoso
    else:
        form = RegistroClienteForm()
    return render(request, 'registro/registro.html', {'form': form})


def confirmacion_registro(request):
    return render(request, 'registro/confirmacion_registro.html')

class Login(View):
    def get(self, request):
        return render(request, 'registro/login.html')

    def post(self, request):
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        user = authenticate(username=correo, password=password)

        if user is not None:
            login(request, user)
            return redirect('pagina_principal')
        else:
            error_message = "Correo electrónico o contraseña incorrectos"
            return render(request, 'registro/login.html', {'error_message': error_message})
        
class RealizarPedidoView(View):
    def get(self, request):
        productos_disponibles = Producto.objects.filter(disponible=True)
        context = {
            'productos': productos_disponibles,
        }
        return render(request, 'principal/realizar_pedido.html', context)

    def post(self, request):
        direccion_entrega = request.POST.get('direccion_entrega')
        forma_pago = request.POST.get('forma_pago')
        productos = request.POST.getlist('productos')
        cantidades = request.POST.getlist('cantidades')

        numero_pedido = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        pedido = Pedido(numero_pedido=numero_pedido, direccion_entrega=direccion_entrega, forma_pago=forma_pago)
        pedido.save()

        for producto_id, cantidad in zip(productos, cantidades):
            producto = Producto.objects.get(id=producto_id)
            detalle_pedido = DetallePedido(pedido=pedido, producto=producto, cantidad=cantidad)
            detalle_pedido.save()

        return redirect('pedido_confirmado')

class HistorialPedidosView(View):
    def get(self, request):
        pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha')

        context = {
            'pedidos': pedidos,
        }
        return render(request, 'principal/historial_pedidos.html', context)

    def post(self, request):
        pedido_id = request.POST.get('pedido_id')

        pedido = Pedido.objects.get(id=pedido_id)

        if pedido.estado in ['pendiente', 'preparacion']:
            pedido.estado = 'cancelado'
            pedido.save()

        return redirect('historial_pedidos')

class CancelarPedidoView(View):
    def post(self, request):
        pedido_id = request.POST.get('pedido_id')

        pedido = Pedido.objects.get(id=pedido_id)

        if pedido.estado in ['pendiente', 'preparacion']:
            pedido.estado = 'cancelado'
            pedido.save()

        return redirect('historial_pedidos')
    
def crear_producto(request):
    if request.method == 'POST':
        form = CrearProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos') 
    else:
        form = CrearProductoForm()
    return render(request, 'crear_producto.html', {'form': form})