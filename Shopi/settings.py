"""
Django settings for Shopi project.
"""

from pathlib import Path
import os


# Shopi/settings.py
LOGIN_URL = '/login/'   # <- correspond à ton URL de login définie
# ==========================================================
# BASE DIR
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# MEDIA & STATIC
# ==========================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # dossier pour les fichiers uploadés

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # dossier pour collectstatic
STATICFILES_DIRS = [BASE_DIR / "static"]  # dossier pour les fichiers statiques du projet

# ==========================================================
# SECURITY
# ==========================================================
SECRET_KEY = 'django-insecure-_s0h8+as&vum@$c^o68of+(=^0r+h!xb!gq(p2rl-yfo4g(ss('
DEBUG = True
ALLOWED_HOSTS = []

# ==========================================================
# AUTHENTICATION
# ==========================================================
# ✅ Correspond au modèle User personnalisé
AUTH_USER_MODEL = 'Administrateur.User'

# ==========================================================
# APPS
# ==========================================================
INSTALLED_APPS = [
    # Apps Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',

    # Mes apps
    'Administrateur',
    'Partenaire',
    'Client',
    'Entreprise',
    'Livreur',
    'Localisation',
    'correspondant',
]

# ==========================================================
# MIDDLEWARE
# ==========================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Shopi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'Shopi.wsgi.application'

# ==========================================================
# DATABASE
# ==========================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==========================================================
# PASSWORD VALIDATION
# ==========================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


CRONJOBS = [
    # exécution toutes les 10 minutes
    ('*/10 * * * *', 'Entreprise.tasks.supprimer_comptes_expirés')
]

# ==========================================================
# INTERNATIONALIZATION
# ==========================================================
LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==========================================================
# DEFAULT AUTO FIELD
# ==========================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================================================
# EMAIL
# ==========================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'moussa21605@gmail.com'
EMAIL_HOST_PASSWORD = 'arzu aijv snay nqdp'  # mot de passe d'application Google
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ==========================================================
# NOM DU SITE
# ==========================================================
NOM_DU_SITE = "SHOPI"