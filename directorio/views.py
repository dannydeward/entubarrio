from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .models import Local, Zona, Categoria, Promocion, Evento

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from .forms import LocalForm

from .forms import PromocionForm
from django.contrib import messages


from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages



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

@login_required
def mi_panel(request):
    mis_locales = Local.objects.filter(usuario=request.user)
    context = {'mis_locales': mis_locales}
    return render(request, 'directorio/mi_panel.html', context)

@login_required
def editar_local(request, local_id):
    local = get_object_or_404(Local, id=local_id)
    if local.usuario != request.user:
        return HttpResponseForbidden("No tienes permiso para editar este local.")
    
    if request.method == 'POST':
        form = LocalForm(request.POST, request.FILES, instance=local)
        if form.is_valid():
            form.save()
            return redirect('directorio:mi_panel')
    else:
        form = LocalForm(instance=local)
    
    context = {'form': form, 'local': local}
    return render(request, 'directorio/editar_local.html', context)


@login_required
def mis_promos(request):
    """Lista las promos del cliente"""
    mis_locales = Local.objects.filter(usuario=request.user)
    promos = Promocion.objects.filter(local__in=mis_locales).order_by('-fecha_inicio')
    return render(request, 'directorio/mis_promos.html', {'promos': promos})

@login_required
def crear_promo(request):
    """Crear nueva promo"""
    mis_locales = Local.objects.filter(usuario=request.user)
    if not mis_locales.exists():
        messages.error(request, "Primero debés tener un local asignado.")
        return redirect('directorio:mi_panel')

    if request.method == 'POST':
        form = PromocionForm(request.POST)
        if form.is_valid():
            promo = form.save(commit=False)
            promo.local = mis_locales.first()  # Asigna al primer local del usuario
            promo.save()
            messages.success(request, "¡Promoción creada con éxito!")
            return redirect('directorio:mis_promos')
    else:
        form = PromocionForm()
    return render(request, 'directorio/form_promo.html', {'form': form, 'titulo': 'Nueva Promoción'})

@login_required
def editar_promo(request, promo_id):
    """Editar promo existente"""
    promo = get_object_or_404(Promocion, id=promo_id, local__usuario=request.user)
    if request.method == 'POST':
        form = PromocionForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            messages.success(request, "Promoción actualizada.")
            return redirect('directorio:mis_promos')
    else:
        form = PromocionForm(instance=promo)
    return render(request, 'directorio/form_promo.html', {'form': form, 'titulo': 'Editar Promoción'})

@login_required
def eliminar_promo(request, promo_id):
    """Eliminar promo"""
    promo = get_object_or_404(Promocion, id=promo_id, local__usuario=request.user)
    if request.method == 'POST':
        promo.delete()
        messages.success(request, "Promoción eliminada.")
    return redirect('directorio:mis_promos')


from .forms import LocalForm, PromocionForm, EventoForm # <--- Agrega EventoForm



@login_required
def mis_eventos(request):
    mis_locales = Local.objects.filter(usuario=request.user)
    eventos = Evento.objects.filter(local__in=mis_locales).order_by('-fecha')
    return render(request, 'directorio/mis_eventos.html', {'eventos': eventos})

@login_required
def crear_evento(request):
    mis_locales = Local.objects.filter(usuario=request.user)
    if not mis_locales.exists():
        messages.error(request, "Primero debés tener un local asignado.")
        return redirect('directorio:mi_panel')

    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.local = mis_locales.first()
            evento.save()
            messages.success(request, "¡Evento creado con éxito!")
            return redirect('directorio:mis_eventos')
    else:
        form = EventoForm()
    return render(request, 'directorio/form_evento.html', {'form': form, 'titulo': 'Nuevo Evento'})

@login_required
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, local__usuario=request.user)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, "Evento eliminado.")
    return redirect('directorio:mis_eventos')


from django.core.mail import send_mail
from django.conf import settings

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        
        # Envía el mail (ahora mismo se imprime en la consola de VS Code)
        send_mail(
            subject=f"Contacto EnTuBarrio: {asunto}",
            message=f"De: {nombre} ({email})\n\n{mensaje}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['dataconeccion@gmail.com'], # Tu email
            fail_silently=False,
        )
        messages.success(request, "¡Mensaje enviado con éxito! Te responderemos pronto.")
        return redirect('directorio:contacto')
        
    return render(request, 'directorio/contacto.html')


def seleccionar_tipo(request):
    return render(request, 'directorio/seleccionar_tipo.html')

def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('directorio:inicio')
    else:
        form = UserCreationForm()
    return render(request, 'directorio/registro.html', {'form': form})

from django.contrib.auth.forms import UserCreationForm

def registro_vecino(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('directorio:login')
    else:
        form = UserCreationForm()
    return render(request, 'directorio/registro_vecino.html', {'form': form})


class LoginVecinoView(LoginView):
    template_name = 'directorio/login_vecino.html'
    redirect_authenticated_user = True


def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        
        send_mail(
            subject=f"Contacto EnTuBarrio: {asunto}",
            message=f"De: {nombre} ({email})\n\n{mensaje}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['dataconeccion@gmail.com'],
            fail_silently=False,
        )
        messages.success(request, "¡Mensaje enviado! Te responderemos pronto.")
        return redirect('directorio:contacto')
        
    return render(request, 'directorio/aparecer.html')