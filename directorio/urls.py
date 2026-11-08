from django.urls import path
from . import views

app_name = 'directorio'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('locales/', views.lista_locales, name='lista_locales'),
    path('locales/<int:local_id>/', views.detalle_local, name='detalle_local'),
    
    path('zonas/', views.lista_zonas, name='lista_zonas'),
    path('zonas/<int:zona_id>/', views.locales_por_zona, name='locales_por_zona'),
    
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/<int:categoria_id>/', views.locales_por_categoria, name='locales_por_categoria'),
    
    # Rutas que apuntan a la página "En construcción"
    path('mapa/', views.en_construccion, name='mapa'),
    path('promos/', views.en_construccion, name='lista_promos'),
    path('eventos/', views.en_construccion, name='eventos'),
    path('contacto/', views.en_construccion, name='contacto'),
    path('crear-admin/', views.crear_admin),
]