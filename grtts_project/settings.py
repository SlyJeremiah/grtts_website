"""
Django settings for the GRTTS website.

Configuration is driven by environment variables (see .env.example).
Production runs on Vercel's Python runtime with PostgreSQL and Backblaze B2.
"""

import os
from pathlib import Path

import dj_database_url
import environ
from django.core.exceptions import ImproperlyConfigured

env = environ.Env(
    DEBUG=(bool, False),
)

BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file if it exists (for local development)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env('DEBUG', default=False)

# Security
SECRET_KEY = env('SECRET_KEY', default=None)
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'django-insecure-local-development-only'
    else:
        raise ImproperlyConfigured(
            'SECRET_KEY must be set in the environment when DEBUG is False. '
            'Generate one with: python -c "from django.core.management.utils '
            'import get_random_secret_key; print(get_random_secret_key())"'
        )

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[
    'grtts.co.zw',
    'www.grtts.co.zw',
    '.vercel.app',
    'localhost',
    '127.0.0.1',
])

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[
    'https://grtts.co.zw',
    'https://www.grtts.co.zw',
    'https://*.vercel.app',
])

# Vercel terminates TLS at the edge and forwards the original scheme.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'SAMEORIGIN'  # django-admin-interface uses same-origin iframes
SILENCED_SYSTEM_CHECKS = ['security.W019']

# Email
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_TIMEOUT = env.int('EMAIL_TIMEOUT', default=10)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default=f'GRTTS <{EMAIL_HOST_USER}>')

# Where enquiries, applications and contact form submissions are delivered.
CONTACT_RECIPIENT = env('CONTACT_RECIPIENT', default='shanyaslym19@gmail.com')
CONTACT_CC = env.list('CONTACT_CC', default=['grttsrangers@gmail.com'])

# Application definition
INSTALLED_APPS = [
    'admin_interface',        # Must come before django.contrib.admin
    'colorfield',             # Must come before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'main',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'grtts_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.partners',
                'main.context_processors.site_facts',
            ],
        },
    },
]

WSGI_APPLICATION = 'grtts_project.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

AUTH_USER_MODEL = 'main.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Africa/Harare'
USE_I18N = True
USE_TZ = True

# Static files
#
# static/ is committed and served directly by Vercel's CDN (see vercel.json).
# WhiteNoise covers local runs with DEBUG=False and any path the CDN misses.
# Do not enable a hashing storage backend without also changing that routing.
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'main/static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Serve straight from STATICFILES_DIRS so a collectstatic run is not required
# for WhiteNoise to work locally or on a deploy where staticfiles/ is absent.
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG

# Media storage: local filesystem in development, Backblaze B2 in production.
if DEBUG:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = env('B2_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('B2_APPLICATION_KEY')
    AWS_STORAGE_BUCKET_NAME = env('B2_BUCKET_NAME', default='grtts-media')
    AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL', default='https://s3.us-east-005.backblazeb2.com')
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-005')
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_ADDRESSING_STYLE = 'virtual'
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # Presigned URLs expire, which breaks CDN caching, image SEO and social
    # previews for public marketing media. Set B2_SIGNED_URLS=False once the
    # bucket serving public assets is made publicly readable.
    AWS_QUERYSTRING_AUTH = env.bool('B2_SIGNED_URLS', default=True)
    AWS_QUERYSTRING_EXPIRE = env.int('B2_URL_EXPIRY', default=3600)

# Uploads — applicant documents and CVs.
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10 MB

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging — Vercel captures stdout/stderr.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '{levelname} {name} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'},
    },
    'root': {'handlers': ['console'], 'level': env('LOG_LEVEL', default='INFO')},
    'loggers': {
        'django.request': {'handlers': ['console'], 'level': 'ERROR', 'propagate': False},
    },
}
