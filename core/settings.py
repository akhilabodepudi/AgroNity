from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    """Read a boolean flag from the environment."""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


def env_list(name):
    """Read a comma-separated list from the environment."""
    return [item.strip() for item in os.environ.get(name, '').split(',') if item.strip()]


# ---------------------------------------------------------------------------
# Environment / deployment detection
# ---------------------------------------------------------------------------
# Vercel automatically sets VERCEL=1 and VERCEL_URL on its build/runtime.
ON_VERCEL = bool(os.environ.get('VERCEL') or os.environ.get('VERCEL_URL'))
VERCEL_URL = os.environ.get('VERCEL_URL')  # e.g. "my-app.vercel.app"

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
# Secret key comes from the environment in production; a dev fallback keeps
# local development frictionless. Never commit a real secret to source control.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-only-change-later')

# DEBUG defaults to False in production (on Vercel) and True locally.
# It can always be overridden explicitly with DJANGO_DEBUG.
DEBUG = env_bool('DJANGO_DEBUG', default=not ON_VERCEL)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.localhost']
ALLOWED_HOSTS.append('.vercel.app')  # all Vercel preview/production domains
if VERCEL_URL:
    ALLOWED_HOSTS.append(VERCEL_URL)
ALLOWED_HOSTS += env_list('DJANGO_ALLOWED_HOSTS')

# CSRF: trust the Vercel HTTPS origins (and any custom domains via env).
CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app']
if VERCEL_URL:
    CSRF_TRUSTED_ORIGINS.append(f'https://{VERCEL_URL}')
CSRF_TRUSTED_ORIGINS += env_list('DJANGO_CSRF_TRUSTED_ORIGINS')

# Vercel terminates TLS at its edge and forwards the original scheme here.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Harden cookies only in production so local HTTP development keeps working.
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'market',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise must sit immediately after SecurityMiddleware.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # global templates
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

WSGI_APPLICATION = 'core.wsgi.application'

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
# Local development uses the bundled SQLite database. In production, set the
# DATABASE_URL environment variable (PostgreSQL) and it will be used instead.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url

    DATABASES['default'] = dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=True,
    )

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files (CSS, JavaScript, images) — served via WhiteNoise
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Vercel runs `collectstatic` automatically during the build when STATIC_ROOT
# is set, then serves the collected files from its CDN. WhiteNoise serves them
# for local `runserver` / `vercel dev`.
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        # Compressed + hashed WhiteNoise storage (supported by Vercel's Django
        # runtime). Serves cache-busted, pre-compressed static assets.
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# ---------------------------------------------------------------------------
# Media files (user uploads, e.g. crop images)
# ---------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Optional cloud media storage for production (env-driven, no hardcoded creds).
# Vercel's serverless filesystem is ephemeral, so local MEDIA_ROOT is NOT a
# durable place to keep uploads in production. To enable Cloudinary, add
# `cloudinary` and `django-cloudinary-storage` to requirements.txt and set the
# CLOUDINARY_URL environment variable. If the package isn't installed, this
# silently no-ops and local media behaviour is preserved.
if os.environ.get('CLOUDINARY_URL'):
    try:
        import cloudinary_storage  # noqa: F401

        INSTALLED_APPS += ['cloudinary_storage', 'cloudinary']
        STORAGES['default'] = {
            'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
        }
    except ImportError:
        pass

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
APPEND_SLASH = True
