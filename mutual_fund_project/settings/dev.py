from .base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ubiz6%-20291r8-$x5*k#0=xgyy=b*7!68(aa4zd%in4h0k=gc'

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Celery configurations
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
