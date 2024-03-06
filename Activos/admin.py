from django.contrib import admin, messages
from .models import *
# Register your models here.

class ActivoAdmin(admin.ModelAdmin):
    list_display = ('id','tic','usuario','condicion','garantia','nombre_equipo')

    # def delete_model(self, request, obj):
    #     try:
    #         obj.delete()
    #     except models.ProtectedError:
    #         messages.error(request, f"No se puede borrar {obj} ya que tiene relaciones con otros registros.")
    #         return

admin.site.register(Activo, ActivoAdmin)

class ActaAdmin(admin.ModelAdmin):
    list_display = ('id','usuario','ruta')

admin.site.register(Acta, ActaAdmin)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','cedula','telefono','area','cargo','ciudad')

admin.site.register(Usuario, UsuarioAdmin)

class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'telefono', 'nombre_contacto', 'correo')

admin.site.register(Proveedor, ProveedorAdmin)


class LicenciaAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('nombre', 'version', 'estado','key','fecha_vigencia',)
    list_filter = ('estado',)
    list_editable = ('estado',)

admin.site.register(Licencia, LicenciaAdmin)

class Tipos_LicenciaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')

admin.site.register(Tipos_Licencia, Tipos_LicenciaAdmin)

class Tipos_ActivosAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')

admin.site.register(Tipos_Activos, Tipos_ActivosAdmin)

class CiudadAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')

admin.site.register(Ciudad, CiudadAdmin)

class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')

admin.site.register(Ubicacion, UbicacionAdmin)

class DireccionAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')

admin.site.register(Direccion, DireccionAdmin)

class AreaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')

admin.site.register(Area, AreaAdmin)

class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')

admin.site.register(Estado, EstadoAdmin)

class MarcaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')

admin.site.register(Marca, MarcaAdmin)

class CargoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')

admin.site.register(Cargo, CargoAdmin)

class CondicionAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')

admin.site.register(Condicion, CondicionAdmin)


admin.site.register(Encabezado)



