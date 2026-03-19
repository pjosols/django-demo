from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'demo-key'
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "::1"]

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'laureates.apps.LaureatesConfig',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'demo.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': ['django.template.context_processors.request']},
}]

WSGI_APPLICATION = 'demo.wsgi.application'
DATABASES = {}

STATIC_URL = '/static/'

USE_I18N = False
USE_TZ = False
