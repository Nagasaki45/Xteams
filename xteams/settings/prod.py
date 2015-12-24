from random import SystemRandom
from .base import *

KEY_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = ''.join([SystemRandom().choice(KEY_CHARS) for i in range(50)])

# The db docker container
DATABASES['default']['HOST'] = 'db'

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Collect static to a mounted volume
STATIC_ROOT = '/staticfiles'
