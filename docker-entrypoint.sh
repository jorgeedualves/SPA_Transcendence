#!/bin/sh

python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py migrate

export DJANGO_SETTINGS_MODULE=core.settings

echo "Starting server"
daphne -b 0.0.0.0 -p 8000 core.asgi:application