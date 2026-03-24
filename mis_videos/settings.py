"""
Configuración del proyecto Django "Mis Videos" - Pro-Gol Watch
Avance 3: Integración con PostgreSQL
"""

from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta del proyecto
SECRET_KEY = 'django-insecure-pro-gol-watch-clave-secreta-2024'

# Modo debug activo durante desarrollo
DEBUG = True

ALLOWED_HOSTS = ['*']

# Aplicaciones instaladas en el proyecto
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'videos',  # Nuestra aplicación de videos
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mis_videos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mis_videos.wsgi.application'

# ─────────────────────────────────────────────────────────────
# BASE DE DATOS PostgreSQL → Pro_Gol
# ─────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME': 'pro_gol',
        'USER':     'postgres',
        'PASSWORD': 'Wwllaptcko061',
        'HOST':     'localhost',
        'PORT':     '5432',
    }
}

# Internacionalización
LANGUAGE_CODE = 'es-mx'
TIME_ZONE     = 'America/Mexico_City'
USE_I18N      = True
USE_TZ        = True

# Archivos estáticos
STATIC_URL = '/static/'

# Tipo de campo clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [BASE_DIR / 'static']



TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']

import os
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
