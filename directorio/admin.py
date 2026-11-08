from django.contrib import admin
from .models import Zona, Categoria, Local, Promocion


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region')
    list_filter = ('region',)
    search_fields = ('nombre',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'icono')
    list_filter = ('tipo',)
    search_fields = ('nombre',)


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'zona', 'categoria', 'es_activo', 'es_destacado')
    list_filter = ('es_activo', 'es_destacado', 'zona', 'categoria')
    search_fields = ('nombre', 'descripcion_corta', 'direccion')
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'zona', 'categoria', 'es_activo', 'es_destacado')
        }),
        ('Descripción', {
            'fields': ('descripcion_corta', 'descripcion_completa', 'dato_curioso')
        }),
        ('Ubicación', {
            'fields': ('direccion', 'latitud', 'longitud')
        }),
        ('Contacto', {
            'fields': ('instagram', 'whatsapp', 'telefono', 'email', 'sitio_web')
        }),
        ('Horarios', {
            'fields': ('horarios',),
            'description': 'Ej: Lun a Vie 9-18hs, Sáb 10-14hs. Domingos cerrado.'
        }),
        ('Imágenes', {
            'fields': ('imagen', 'foto1', 'foto2', 'foto3'),
            'description': 'Imagen principal + 3 fotos adicionales del cliente'
        }),
    )


@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'local', 'fecha_inicio', 'fecha_fin', 'es_activa')
    list_filter = ('es_activa', 'local')
    search_fields = ('titulo', 'descripcion')