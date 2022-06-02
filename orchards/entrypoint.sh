#!/bin/sh

cd /home/aero/app/
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

# serve using uwsgi with nginx
uwsgi --socket :8005 --module orchards.wsgi --chmod-socket=660 --processes=3 --uid=aero --gid=aero --logto=/var/log/uwsgi/aero.log --master 