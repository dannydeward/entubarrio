from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('aparecer/', views.contacto, name='aparecer'),

      # --- NUEVAS RUTAS DEL PANEL DE AUTOGESTIÓN ---
    path('mi-panel/', views.mi_panel, name='mi_panel'),
    path('editar-local/<int:local_id>/', views.editar_local, name='editar_local'),
    
    path('login/', auth_views.LoginView.as_view(template_name='directorio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Promociones del cliente
    path('mis-promos/', views.mis_promos, name='mis_promos'),
    path('crear-promo/', views.crear_promo, name='crear_promo'),
    path('editar-promo/<int:promo_id>/', views.editar_promo, name='editar_promo'),
    path('eliminar-promo/<int:promo_id>/', views.eliminar_promo, name='eliminar_promo'),


    path('mis-eventos/', views.mis_eventos, name='mis_eventos'),
    path('crear-evento/', views.crear_evento, name='crear_evento'),
    path('eliminar-evento/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),

    path('seleccionar/', views.seleccionar_tipo, name='seleccionar_tipo'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('registro/', views.registro_vecino, name='registro_vecino'),

    

# ... dentro de urlpatterns ...
path('cambiar-clave/', auth_views.PasswordChangeView.as_view(template_name='directorio/cambiar_clave.html', success_url='/cambiar-clave/done/'), name='cambiar_clave'),
path('cambiar-clave/done/', auth_views.PasswordChangeDoneView.as_view(template_name='directorio/cambiar_clave_done.html'), name='cambiar_clave_done'),
  
     
]