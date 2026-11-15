
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
    list_filter = ('zona', 'categoria', 'es_activo', 'es_destacado')
    search_fields = ('nombre', 'direccion', 'descripcion_corta')
    list_editable = ('es_activo', 'es_destacado')


@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'local', 'fecha_inicio', 'fecha_fin', 'es_activa')
    list_filter = ('es_activa', 'fecha_inicio')
    search_fields = ('titulo', 'local__nombre')
