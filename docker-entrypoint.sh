#!/bin/bash

python manage.py migrate
gunicorn redirekt.wsgi --bind 0.0.0.0:8000
