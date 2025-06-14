"""
Django settings for freshfutures project.

Generated by 'django-admin startproject' using Django 5.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url

# operating system environment
# os.environ['GDAL_LIBRARY_PATH'] = '/usr/lib/libgdal.so'

# load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Manual .env loading (more reliable than python-dotenv in this context)
env_file = BASE_DIR / '.env'

if env_file.exists():
    with open(env_file, 'r') as f:
        content = f.read()
        
    with open(env_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value  # Use direct assignment instead of setdefault
                


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# Mapbox Configuration
MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')

# SECURITY WARNING: don't run with debug turned on in production!

# Updated from this because I was getting errors in deployment re debug being undefined when in heroku
# if not 'ON_HEROKU' in os.environ:
#     DEBUG = True
    
if 'ON_HEROKU' in os.environ:
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS=['https://*.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'main_app',
    'accounts',
    'django.contrib.gis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'freshfutures.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
           BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Add this line to make mapbox_token available in all templates
                'main_app.context_processors.mapbox_token',
            ],
        },
    },
]

WSGI_APPLICATION = 'freshfutures.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# From GA instructions:
# if 'ON_HEROKU' in os.environ:
#     DATABASES = {
#         "default": dj_database_url.config(
#             env='DATABASE_URL',
#             conn_max_age=600,
#             conn_health_checks=True,
#             ssl_require=True,
#         ),
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': 'fresh_futures_db',
#         }
#     }

# From ChatGPT about database for Heroku with PostGIS
if 'ON_HEROKU' in os.environ:
    DATABASES = {
        "default": dj_database_url.config(
            env='DATABASE_URL',
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
            engine='django.contrib.gis.db.backends.postgis',
        ),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'fresh_futures_db',
            # 'USER': 'annam',
            # 'PASSWORD': '',
            # 'HOST': 'localhost',
            # 'PORT': '5432',
            # Add USER, PASSWORD, HOST, PORT if needed
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators


# Uncomment the following lines below to enable password validation checks/constraints
# This is optional and can be customized based on future goals for the project
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [
    BASE_DIR / 'main_app' / 'static',  # Tell Django to look in main_app/static
]

# For development
if DEBUG:
    STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Adding to support AbstractUser
AUTH_USER_MODEL = 'main_app.User'

