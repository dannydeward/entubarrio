from django import forms
from .models import Local, Promocion, Evento

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        # Solo permitimos editar estos campos. 
        # Zona, Categoría, es_activo, etc., quedan bloqueadas para el cliente.
        fields = [
            'nombre', 
            'descripcion_corta', 
            'descripcion_completa', 
            'direccion', 
            'instagram', 
            'whatsapp', 
            'telefono', 
            'email', 
            'sitio_web', 
            'horarios', 
            'foto1', 'foto2', 'foto3', 
            'dato_curioso', 
            'imagen'
        ]
        widgets = {
            'descripcion_corta': forms.Textarea(attrs={'rows': 3}),
            'descripcion_completa': forms.Textarea(attrs={'rows': 5}),
            'horarios': forms.Textarea(attrs={'rows': 3}),
        }



class PromocionForm(forms.ModelForm):
    class Meta:
            model = Promocion
            fields = ['titulo', 'descripcion', 'precio_especial', 'fecha_inicio', 'fecha_fin', 'fuente']
            widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }



class EventoForm(forms.ModelForm):
    class Meta:
         model = Evento
         fields = ['titulo', 'descripcion', 'fecha', 'hora']
         widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }