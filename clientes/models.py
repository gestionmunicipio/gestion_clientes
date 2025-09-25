from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

### Importar planilla de clientes #### 
from django.contrib.auth import get_user_model

#--- devuelve la clase del modelo de usuario activo en tu proyecto Django
User = get_user_model()


class AgenteVentas(models.Model):
    # Nueva relación uno a uno con User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agente_perfil',
        null=True,
        blank=True,
        verbose_name=_("Usuario")
    )

    nombre = models.CharField(max_length=100, verbose_name=_("Nombre"))
    rut = models.CharField(max_length=20, unique=True, verbose_name=_("Rut"))
    email = models.EmailField(unique=True, verbose_name=_("Correo Electrónico"))
    telefono = models.CharField(max_length=15, verbose_name=_("Teléfono"))

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Agente de ventas"
        verbose_name_plural = "Agentes de ventas"


class TipoEntidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name=_("Tipo de Entidad"))

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    tipo_entidad = models.ForeignKey(TipoEntidad, on_delete=models.SET_NULL, null=True, verbose_name=_("Tipo de Entidad"))
    nombre_razon_social = models.CharField(max_length=200, blank=True, verbose_name=_("Nombre o Razón Social"))
    rut = models.CharField(max_length=20, unique=True, verbose_name=_("Rut"))
    email = models.EmailField(unique=True, verbose_name=_("Correo Electrónico"))
    telefono = models.CharField(max_length=15, verbose_name=_("Teléfono"))
    sitio_web = models.CharField(max_length=100, blank=True, verbose_name=_("Sitio Web"))
    activo = models.BooleanField(default=True, verbose_name=_("Activo"))
    observacion = models.TextField(blank=True, verbose_name=_("Observación"))
    agente = models.ForeignKey(AgenteVentas, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre_razon_social

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class TipoDireccion(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name=_("Tipo de Dirección"))
    descripcion = models.TextField(blank=True, verbose_name=_("Descripción"))

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name =_("Tipo de Dirección")
        verbose_name_plural =_("Tipos de Direcciones")


class Direccion(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='direcciones')
    tipo = models.ForeignKey('TipoDireccion', on_delete=models.PROTECT, verbose_name=_("Tipo de Dirección"))
    calle = models.CharField(max_length=100, verbose_name=_("Calle"))
    numero = models.CharField(max_length=20, verbose_name=_("Número"))
    comuna = models.CharField(max_length=100, verbose_name=_("Comuna"))
    ciudad = models.CharField(max_length=100, verbose_name=_("Ciudad"))
    codigo_postal = models.CharField(max_length=20, blank=True, verbose_name=_("Código Potal"))
    pais = models.CharField(max_length=100, verbose_name=_("País"))
    observacion = models.TextField(blank=True, verbose_name=_("Observación"))

    def __str__(self):
        return f"{self.tipo} - {self.calle} {self.numero}, {self.comuna}"
    
    class Meta:
        verbose_name =_("Dirección")
        verbose_name_plural =_("Direcciones")


#=================================================
# Modelo para rastrear cada carga en la Importación
#=================================================
class ImportacionLog(models.Model):
    archivo       = models.FileField(upload_to='importaciones/')
    fecha         = models.DateTimeField(auto_now_add=True)
    usuario       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    exitosos      = models.PositiveIntegerField(default=0)
    fallidos      = models.PositiveIntegerField(default=0)
    errores       = models.TextField(blank=True)   # JSON o texto plano con detalle por fila
    hash_archivo  = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.archivo.name} @ {self.fecha:%Y-%m-%d %H:%M}"

    class Meta:
        ordering = ['-fecha']

