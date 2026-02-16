import os
import dj_database_url
from pathlib import Path
import environ
import pymysql
pymysql.install_as_MySQLdb()

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False)
)

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file if it exists (for local development)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='your-secret-key-here-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)

# Allowed hosts - Updated for Vercel
ALLOWED_HOSTS = [
    '.vercel.app',
    '.now.sh',
    'localhost',
    '127.0.0.1',
    'grtts.co.zw',
    'www.grtts.co.zw',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'main',
    'blog',

    # For file storage (storages app)
    'storages',
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

# Templates Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'main/templates'),
            os.path.join(BASE_DIR, 'blog/templates'),
        ],
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

WSGI_APPLICATION = 'grtts_project.wsgi.application'

# Database - Configure for Vercel (PostgreSQL recommended)
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
]

# Custom user model
AUTH_USER_MODEL = 'main.User'

# Login/Logout URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Harare'
USE_I18N = True
USE_TZ = True

# ========== FILE STORAGE CONFIGURATION ==========
if DEBUG:
    # Development: Use local storage
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
    # Create media directories if they don't exist
    os.makedirs(MEDIA_ROOT, exist_ok=True)
    os.makedirs(os.path.join(MEDIA_ROOT, 'blog'), exist_ok=True)
    os.makedirs(os.path.join(MEDIA_ROOT, 'courses'), exist_ok=True)
    os.makedirs(os.path.join(MEDIA_ROOT, 'testimonials'), exist_ok=True)
    os.makedirs(os.path.join(MEDIA_ROOT, 'locations'), exist_ok=True)
else:
    # Production: Use Backblaze B2 with private bucket and signed URLs
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    # Your Backblaze credentials
    AWS_ACCESS_KEY_ID = env('B2_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('B2_APPLICATION_KEY')
    AWS_STORAGE_BUCKET_NAME = env('B2_BUCKET_NAME', default='grtts-media')
    
    # Backblaze B2 endpoint
    AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL', default='https://s3.us-east-005.backblazeb2.com')
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-005')
    
    # S3-compatible settings
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_ADDRESSING_STYLE = 'virtual'
    
    # Settings for private bucket with signed URLs
    AWS_QUERYSTRING_AUTH = True
    AWS_QUERYSTRING_EXPIRE = 3600  # URLs valid for 1 hour
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    
    # Media URL is not set - backend generates signed URLs
    MEDIA_URL = None
# ========== END FILE STORAGE CONFIGURATION ==========

# ========== STATIC FILES CONFIGURATION ==========
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'main/static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Single source of truth for static files storage
if os.environ.get('VERCEL'):
    # On Vercel, use Django's manifest storage for hashed files
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
elif DEBUG:
    # Local development - simple storage for easy debugging
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    # Local production simulation - WhiteNoise with compression
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# ========== END STATIC FILES CONFIGURATION ==========

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Allowed file types
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
ALLOWED_FILE_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/plain',
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='shanyaslym19@gmail.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = 'GRTTS <info@grtts.co.zw>'

# Admin email notifications
ADMIN_EMAILS = ['shanyaslym19@gmail.com']

# Site URL for email links
SITE_URL = env('SITE_URL', default='https://grtts-website.vercel.app')

# ========== VERCEL SECURITY SETTINGS ==========
if os.environ.get('VERCEL'):
    # Security settings for Vercel
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # CSRF trusted origins
    CSRF_TRUSTED_ORIGINS = [
        'https://*.vercel.app',
        'https://*.now.sh',
        'https://grtts.co.zw',
        'https://www.grtts.co.zw',
    ]
else:
    # Local development security settings
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
# ========== END VERCEL SETTINGS ==========

# Payment Gateway Settings
PAYNOW_INTEGRATION_ID = env('PAYNOW_INTEGRATION_ID', default='')
PAYNOW_INTEGRATION_KEY = env('PAYNOW_INTEGRATION_KEY', default='')

ECOCASH_API_KEY = env('ECOCASH_API_KEY', default='')
ECOCASH_API_SECRET = env('ECOCASH_API_SECRET', default='')

ONEMONEY_MERCHANT_CODE = env('ONEMONEY_MERCHANT_CODE', default='')
ONEMONEY_API_KEY = env('ONEMONEY_API_KEY', default='')

# Payment test mode
PAYMENT_TEST_MODE = env.bool('PAYMENT_TEST_MODE', default=True)
