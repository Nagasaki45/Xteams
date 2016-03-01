from random import SystemRandom
from .base import *

KEY_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = ''.join([SystemRandom().choice(KEY_CHARS) for i in range(50)])

DEBUG = False

# The db docker container
DATABASES['default']['HOST'] = 'db'

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Gzip statics
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
