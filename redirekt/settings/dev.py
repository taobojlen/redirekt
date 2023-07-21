import os

from .core import *

HOSTNAME = "localhost:8000"
DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = "development secret key"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
DJANGO_VITE_DEV_MODE = True