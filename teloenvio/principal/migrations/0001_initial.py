# Generated by Django 4.2.1 on 2023-07-11 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fono', models.CharField(max_length=20)),
                ('correo', models.EmailField(max_length=254)),
                ('nombre', models.CharField(max_length=100)),
                ('numIdentificador', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=200)),
                ('comuna', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Productor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreContacto', models.CharField(max_length=100)),
                ('RUT', models.CharField(max_length=20)),
                ('razonSocial', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('comuna', models.CharField(max_length=100)),
                ('rubro', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcionProducto', models.CharField(max_length=200)),
                ('precioProducto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('imagenProducto', models.ImageField(upload_to='productos/')),
                ('stockProducto', models.PositiveIntegerField()),
                ('idProductor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.productor')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_pedido', models.CharField(max_length=50, unique=True)),
                ('direccion_entrega', models.CharField(max_length=200)),
                ('forma_pago', models.CharField(max_length=100)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_revision', 'En Revisión'), ('enviado', 'Enviado'), ('entregado', 'Entregado')], max_length=20)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.producto')),
            ],
        ),
    ]