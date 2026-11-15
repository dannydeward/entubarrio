from django.db import migrations

def cargar_barrios_caba(apps, schema_editor):
    Zona = apps.get_model('directorio', 'Zona')
    
    barrios_caba = [
        'Agronomía', 'Almagro', 'Balvanera', 'Barracas', 'Belgrano', 'Boedo',
        'Caballito', 'Chacarita', 'Coghlan', 'Colegiales', 'Constitución',
        'Flores', 'Floresta', 'La Boca', 'La Paternal', 'Liniers',
        'Mataderos', 'Monte Castro', 'Monserrat', 'Nueva Pompeya', 'Núñez',
        'Palermo', 'Parque Avellaneda', 'Parque Chacabuco', 'Parque Chas',
        'Parque Patricios', 'Puerto Madero', 'Recoleta', 'Retiro', 'Saavedra',
        'San Cristóbal', 'San Nicolás', 'San Telmo', 'Vélez Sarsfield',
        'Versalles', 'Villa Crespo', 'Villa del Parque', 'Villa Devoto',
        'Villa General Mitre', 'Villa Lugano', 'Villa Luro', 'Villa Ortúzar',
        'Villa Pueyrredón', 'Villa Real', 'Villa Riachuelo', 'Villa Santa Rita',
        'Villa Soldati', 'Villa Urquiza'
    ]
    
    for barrio in barrios_caba:
        Zona.objects.get_or_create(
            nombre=barrio,
            defaults={'region': 'CABA'}
        )

class Migration(migrations.Migration):
    dependencies = [
        ('directorio', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(cargar_barrios_caba),
    ]