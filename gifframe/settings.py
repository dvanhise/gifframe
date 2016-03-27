
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import requests
from boto.s3.connection import S3Connection, OrdinaryCallingFormat

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h4azs6ck(n$7shm@b_uq60x*k+8vuhl&^eu3u48@7ez_y+&9pm'

AWS_ACCESS_KEY_ID = 'AKIAIG7ZDOVVCIAGUSGA'
AWS_SECRET_ACCESS_KEY = '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'
MAIN_BUCKET = 'images.gifframe.test'

AWS_CONNECTION = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, calling_format=OrdinaryCallingFormat())

if not AWS_CONNECTION:
    raise requests.ConnectionError

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gifframe'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'gifframe.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'gifframe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = ''
STATIC_URL = '/static/'

# This is needed for serving static files on windows machines
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"), )
