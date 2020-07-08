#!/bin/sh
set -e
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9090 --workers 4 --master --enable-threads --module app.wsgi
