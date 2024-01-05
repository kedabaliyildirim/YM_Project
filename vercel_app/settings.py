"""
Django settings for vercel_app project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import dotenv
import os
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv.load_dotenv()
secret = os.getenv("SECRET_KEY")
secureConnection = os.getenv("SECURE_CONNECTION")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = f'{secret}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app',
                 'http://localhost:5173','http://localhost:5175', '14b4-188-3-98-176.ngrok-free.app']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_extensions',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'worth2watch',
    'corsheaders'
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
ROOT_URLCONF = 'vercel_app.urls'
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_METHODS = ['GET', 'POST', 'OPTIONS']
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5175",
    "http://localhost:5173",
    "https://github.com",
    "http://localhost:5173",
    "https://worth2-watch-front-end.vercel.app",
    # Add the URL of your Vue.js app
    "https://worth2-watch-front-jr6f9olki-kedabaliyildirims-projects.vercel.app"
    # Add other allowed origins as needed
]
CORS_ALLOW_HEADERS = [
    'X-CSRF-TOKEN',
    'content-type',
    'x-csrftoken',
    "csrfToken",
    'csrf_token',
    'x-csrf-token',
    'X-CSRFTOKEN'
]
CSRF_COOKIE_DOMAIN = [' http://localhost:5173']
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5175",
    "http://localhost:5173",
    "http://localhost:5173",
    "https://worth2-watch-front-end.vercel.app"  # Add the URL of your Vue.js app
]
CORS_ALLOWED_REGEXES = [
    "http://localhost:5175",
    "http://localhost:5173",
    "http://localhost:5173",
    "https://worth2-watch-front-end.vercel.app"  # Add the URL of your Vue.js app
]
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

WSGI_APPLICATION = 'vercel_app.wsgi.app'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# Note: Django modules for using databases are not support in serverless
# environments like Vercel. You can use a database over HTTP, hosted elsewhere.

DATABASES = {}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
