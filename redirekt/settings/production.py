import os

import dj_database_url

from .core import *

SECRET_KEY = os.environ["SECRET_KEY"]
HOSTNAME = os.environ.get("HOSTNAME", "localhost")
ALLOWED_HOSTS = [HOSTNAME]

DEBUG = False

DATABASES = {"default": dj_database_url.config(conn_max_age=600)}

DJANGO_VITE_DEV_MODE = False