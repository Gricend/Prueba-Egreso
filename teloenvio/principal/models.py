from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from PIL import Image

class Productor(models.Model):
    nombreContacto = models.CharField(max_length=100)
    RUT = models.CharField(max_length=20)
    razonSocial = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    comuna = models.CharField(max_length=100)
    rubro = models.CharField(max_length=100)

class Cliente(models.Model):
    fono = models.CharField(max_length=20)
    correo = models.EmailField()
    nombre = models.CharField(max_length=100)
    numIdentificador = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    comuna = models.CharField(max_length=100)

class Producto(models.Model):
    idProductor = models.ForeignKey(Productor, on_delete=models.CASCADE)
    descripcionProducto = models.CharField(max_length=200)
    precioProducto = models.DecimalField(max_digits=10, decimal_places=2)
    imagenProducto = models.ImageField(upload_to='productos/')
    stockProducto = models.PositiveIntegerField()

    def __str__(self):
        return self.descripciónProducto
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.imagen:
            img = Image.open(self.imagen.path)

            tamano_deseado = (225, 225)

            img.thumbnail(tamano_deseado)
            
            img.save(self.imagen.path)

ESTADOS_PEDIDO = (
    ('pendiente', 'Pendiente'),
    ('en_revision', 'En Revisión'),
    ('enviado', 'Enviado'),
    ('entregado', 'Entregado'),
)

class Pedido(models.Model):
    numero_pedido = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    direccion_entrega = models.CharField(max_length=200)
    forma_pago = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO)

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def subtotal(self):
        return self.cantidad * self.producto.precioProducto

