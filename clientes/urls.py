from django.urls import path
from . import views

"""
app_name = 'clientes'  # 👈 Esto es lo que registra el namespace. Sin ella, el namespace no existe
Se omitirá para no tener conflicto con las otras vistas.
"""

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('nuevo/', views.crear_cliente, name='crear_cliente'),
    path('editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/<int:cliente_id>/direccion/nueva/', views.agregar_direccion, name='agregar_direccion'),
    path('cliente/<int:pk>/eliminar/', views.confirmar_eliminar_cliente, name='confirmar_eliminar_cliente'),
    path('direccion/<int:pk>/editar/', views.editar_direccion, name='editar_direccion'),
    path('direccion/<int:pk>/eliminar/', views.eliminar_direccion, name='eliminar_direccion'),
    path('consulta/', views.consulta_clientes, name='consulta_clientes'),
    path('consulta/exportar-excel/', views.exportar_clientes_excel, name='exportar_clientes_excel'),
    path('consulta/exportar-pdf/', views.exportar_clientes_pdf, name='exportar_clientes_pdf'),
    path('importar/', views.importar_clientes, name='importar_clientes'),
    path('dashboard/', views.dashboard_supervisor, name='dashboard_supervisor'),
]
