
"""
Django settings for guiavene project.
Versión preparada para Render + Neon (Postgres) + Cloudinary.
Requiere Django 4.2 o superior (usa STORAGES).
"""
from pathlib import Path
import os
 
import dj_database_url
 
BASE_DIR = Path(__file__).resolve().parent.parent
 
# --- Seguridad ---------------------------------------------------------
# En Render define SECRET_KEY como variable de entorno (genera una nueva,
# la anterior quedó expuesta).
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-solo-para-desarrollo-local')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
 
ALLOWED_HOSTS = ['entubarrio-3.onrender.com', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://entubarrio-3.onrender.com']
# Render está detrás de un proxy HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
 
# --- Apps --------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',              # debe ir ANTES de staticfiles
    'django.contrib.staticfiles',
    'cloudinary',
    'directorio',
]
 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # justo después de Security
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
 
ROOT_URLCONF = 'guiavene.urls'
 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
 
WSGI_APPLICATION = 'guiavene.wsgi.application'
 
# --- Base de datos -----------------------------------------------------
# Con DATABASE_URL (Neon) usa Postgres; sin ella, SQLite local.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        ssl_require=bool(os.environ.get('DATABASE_URL')),
    )
}
 
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
 
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True
 
# --- Archivos estáticos ------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
 
# --- Archivos media (imágenes subidas desde el admin) ------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
 
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}
 
# Si hay credenciales de Cloudinary, las imágenes van allí;
# si no (desarrollo local), se guardan en la carpeta /media.
if CLOUDINARY_STORAGE['CLOUD_NAME']:
    DEFAULT_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    DEFAULT_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
 
STORAGES = {
    'default': {'BACKEND': DEFAULT_STORAGE},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
 
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'