"""
URL configuration for teloenvio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from principal.views import (
    home, 
    Login,
    RealizarPedidoView,
    HistorialPedidosView, 
    CancelarPedidoView, 
    TomarPedidoView, 
    SeguimientoPedidosView, 
    ActualizarEstadoPedidoView, 
    registro_cliente, 
    confirmacion_registro)

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='Home'),
    path('iniciar_sesion/', Login.as_view(), name='iniciar_sesion'),
    path('realizar_pedido/', RealizarPedidoView.as_view(), name='realizar_pedido'),
    path('historial_pedidos/', HistorialPedidosView.as_view(), name='historial_pedidos'),
    path('cancelar_pedido/', CancelarPedidoView.as_view(), name='cancelar_pedido'),
    path('tomar_pedido/', TomarPedidoView.as_view(), name='tomar_pedido'),
    path('seguimiento_pedidos/', SeguimientoPedidosView.as_view(), name='seguimiento_pedidos'),
    path('actualizar_estado/<int:pedido_id>/', ActualizarEstadoPedidoView.as_view(), name='actualizar_estado'),
    path('registro/', registro_cliente, name='registro_cliente'),
    path('confirmacion_registro/', confirmacion_registro, name='confirmacion_registro'),
    
]
