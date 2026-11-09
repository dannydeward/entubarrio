from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .models import Local, Zona, Categoria, Promocion


from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import connection


def inicio(request):
    """Página principal con locales destacados"""
    locales_destacados = Local.objects.filter(
        es_activo=True
    ).select_related('zona', 'categoria')[:12]
    
    hay_locales_provincia = Local.objects.filter(
        es_activo=True,
        zona__region='PROVINCIA'
    ).exists()
    
    context = {
        'locales_destacados': locales_destacados,
        'hay_locales_provincia': hay_locales_provincia,
    }
    return render(request, 'directorio/inicio.html', context)


def lista_locales(request):
    """Lista de todos los locales con filtros"""
    locales = Local.objects.filter(es_activo=True).select_related('zona', 'categoria')
    
    zona_id = request.GET.get('zona')
    categoria_id = request.GET.get('categoria')
    busqueda = request.GET.get('q')
    
    if zona_id:
        locales = locales.filter(zona__id=zona_id)
    
    if categoria_id:
        locales = locales.filter(categoria__id=categoria_id)
    
    if busqueda:
        locales = locales.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion_corta__icontains=busqueda) |
            Q(direccion__icontains=busqueda)
        )
    
    zonas = Zona.objects.all()
    categorias = Categoria.objects.all()
    
    context = {
        'locales': locales,
        'zonas': zonas,
        'categorias': categorias,
        'zona_actual': zona_id,
        'categoria_actual': categoria_id,
        'busqueda': busqueda,
    }
    return render(request, 'directorio/lista_locales.html', context)


def detalle_local(request, local_id):
    """Página de detalle de un local específico"""
    local = get_object_or_404(
        Local.objects.select_related('zona', 'categoria').prefetch_related('promociones'),
        id=local_id,
        es_activo=True
    )
    
    promos_activas = local.promociones.filter(
        es_activa=True,
        fecha_fin__gte=timezone.now().date()
    )
    
    context = {
        'local': local,
        'promos_activas': promos_activas,
    }
    return render(request, 'directorio/detalle_local.html', context)


def lista_zonas(request):
    """Lista de todas las zonas"""
    zonas = Zona.objects.all()
    
    for zona in zonas:
        zona.total_locales = Local.objects.filter(zona=zona, es_activo=True).count()
    
    context = {
        'zonas': zonas,
    }
    return render(request, 'directorio/lista_zonas.html', context)


def locales_por_zona(request, zona_id):
    """Locales filtrados por zona"""
    zona = get_object_or_404(Zona, id=zona_id)
    locales = Local.objects.filter(zona=zona, es_activo=True).select_related('zona', 'categoria')
    
    zonas = Zona.objects.all()
    categorias = Categoria.objects.all()
    
    context = {
        'locales': locales,
        'zonas': zonas,
        'categorias': categorias,
        'titulo': f'Locales en {zona.nombre}',
    }
    return render(request, 'directorio/lista_locales.html', context)


def locales_por_categoria(request, categoria_id):
    """Locales filtrados por categoría"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    locales = Local.objects.filter(categoria=categoria, es_activo=True).select_related('zona', 'categoria')
    
    zonas = Zona.objects.all()
    categorias = Categoria.objects.all()
    
    context = {
        'locales': locales,
        'zonas': zonas,
        'categorias': categorias,
        'titulo': f'Locales en {categoria.nombre}',
    }
    return render(request, 'directorio/lista_locales.html', context)


def lista_categorias(request):
    """Lista de todas las categorías"""
    categorias = Categoria.objects.all()
    
    for categoria in categorias:
        categoria.total_locales = Local.objects.filter(categoria=categoria, es_activo=True).count()
    
    context = {
        'categorias': categorias,
    }
    return render(request, 'directorio/lista_categorias.html', context)


def mapa(request):
    return render(request, 'directorio/mapa.html')


def lista_promos(request):
    return render(request, 'directorio/lista_promos.html')


def eventos(request):
    return render(request, 'directorio/eventos.html')


def en_construccion(request):
    """Página genérica para secciones que aún no están listas"""
    return render(request, 'directorio/en_construccion.html')





def diagnostico_temporal(request):
    if request.GET.get('clave') != 'verificar-2026':
        return HttpResponse('No autorizado', status=403)

    User = get_user_model()

    usuario = User.objects.filter(username='chu').first()

    resultado = {
        'DATABASE_HOST': connection.settings_dict.get('HOST'),
        'DATABASE_NAME': connection.settings_dict.get('NAME'),
        'USUARIO_CHU_EXISTE': usuario is not None,
        'ES_STAFF': usuario.is_staff if usuario else None,
        'ES_SUPERUSER': usuario.is_superuser if usuario else None,
        'ESTA_ACTIVO': usuario.is_active if usuario else None,
    }

    return HttpResponse(str(resultado), content_type='text/plain')