from django.db import models


class Zona(models.Model):
    REGION_CHOICES = [
        ('CABA', 'Ciudad Autónoma de Buenos Aires (CABA)'),
        ('PROVINCIA', 'Provincia de Buenos Aires'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='CABA')
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Zona / Localidad"
        verbose_name_plural = "Zonas / Localidades"
        ordering = ['region', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_region_display()})"


class Categoria(models.Model):
    TIPO_CHOICES = [
        ('gastronomia', '🍽️ Gastronomía'),
        ('servicios', '💼 Servicios Profesionales'),
        ('servicios_tecnicos', '🔧 Servicios Técnicos'),
        ('diseno_imagen', '🎨 Diseño e Imagen'),
        ('belleza', '💇 Belleza y Bienestar'),
        ('comercios', '🛒 Comercios'),
        ('cultura', '🎭 Cultura y Eventos'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    icono = models.CharField(max_length=10, blank=True, help_text="Emoji o código de ícono")
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['tipo', 'nombre']
    
    def __str__(self):
        return f"{self.icono} {self.nombre}"


class Local(models.Model):
    nombre = models.CharField(max_length=200)
    
    zona = models.ForeignKey(Zona, on_delete=models.SET_NULL, null=True, related_name='locales')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='locales')
    
    descripcion_corta = models.CharField(max_length=300, help_text="Descripción breve para tarjetas")
    descripcion_completa = models.TextField(blank=True, help_text="Descripción detallada")
    direccion = models.CharField(max_length=255)
    
    instagram = models.CharField(
        max_length=150, 
        blank=True, 
        help_text="Usuario de Instagram: ej: @la.perrera_ok, usuario.venezolano"
    )
    whatsapp = models.CharField(max_length=50, blank=True, help_text="Con código de país: +54...")
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    sitio_web = models.URLField(blank=True)
    
    horarios = models.CharField(
        max_length=300, 
        blank=True, 
        help_text="Ej: Lun a Vie 9-18hs, Sáb 10-14hs. Domingos cerrado."
    )
    
    foto1 = models.ImageField(upload_to='locales/fotos/', blank=True, null=True)
    foto2 = models.ImageField(upload_to='locales/fotos/', blank=True, null=True)
    foto3 = models.ImageField(upload_to='locales/fotos/', blank=True, null=True)
    
    dato_curioso = models.TextField(blank=True, help_text="Tip exclusivo del local")
    
    imagen = models.ImageField(upload_to='locales/', blank=True, null=True)
    
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Ej: -34.603722")
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Ej: -58.381592")
    
    es_activo = models.BooleanField(default=True, help_text="¿El local sigue abierto/activo?")
    es_destacado = models.BooleanField(default=False, help_text="¿Aparece en la página principal?")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locales"
        ordering = ['-es_destacado', '-fecha_actualizacion']
    
    def __str__(self):
        return f"{self.nombre} ({self.zona})"


class Promocion(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='promociones')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio_especial = models.CharField(max_length=100, blank=True, help_text="Ej: '$500', '2x1'")
    
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    es_activa = models.BooleanField(default=True)
    fuente = models.URLField(blank=True, help_text="Link al post de Instagram o anuncio")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.local.nombre} - {self.titulo}"