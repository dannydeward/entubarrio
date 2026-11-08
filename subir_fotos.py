import os
import django
import cloudinary

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guiavene.settings')
django.setup()

cloudinary.config(
    cloud_name="wdeufiiu",
    api_key="572733275461677",
    api_secret="sTozNrIkr7L0sLRcaWpRqwGdqUQ"
)

from directorio.models import Local

print("Subiendo fotos a Cloudinary...")
for local in Local.objects.all():
    if local.imagen and str(local.imagen).startswith('locales/'):
        ruta = os.path.join('media', str(local.imagen))
        if os.path.exists(ruta):
            try:
                res = cloudinary.uploader.upload(ruta, folder="locales")
                local.imagen = res['secure_url']
                local.save()
                print(f"✅ {local.nombre}")
            except Exception as e:
                print(f"❌ {local.nombre}: {e}")
print("Listo.")