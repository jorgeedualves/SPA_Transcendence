#!/bin/sh

sleep 15

python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py migrate

export DJANGO_SETTINGS_MODULE=core.settings

echo "Starting server"
daphne -e ssl:443:privateKey=/etc/ssl/private/key.pem:certKey=/etc/ssl/certs/cert.pem core.asgi:application