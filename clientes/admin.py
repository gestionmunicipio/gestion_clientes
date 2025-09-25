from django.contrib import admin
from .models import Direccion, Cliente, AgenteVentas, TipoEntidad

# Tus modelos propios
admin.site.register(Direccion)
admin.site.register(Cliente)
admin.site.register(AgenteVentas)
admin.site.register(TipoEntidad)
