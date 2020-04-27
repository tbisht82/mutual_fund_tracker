from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ubiz6%-20291r8-$x5*k#0=xgyy=b*7!68(aa4zd%in4h0k=gc'

DATABASES['default'] = dj_database_url.config()

# Celery configurations
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://') #, 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://') #, 'redis://localhost:6379')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'