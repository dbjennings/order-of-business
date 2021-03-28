from .base import *

# Debug always True for development
DEBUG = ENV.bool('DJANGO_DEBUG', default=True)

ALLOWED_HOSTS = [
    'testserver',
    'localhost',
]