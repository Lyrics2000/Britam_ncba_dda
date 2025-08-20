#!/usr/bin/env bash


set -e
# python manage.py migrate --noinput

#python property_manager.py collectstatic —-noinput
# first remove the collect static folder
rm -rf static
echo yes | python manage.py collectstatic



# python manage.py runserver 0.0.0.0:9500
exec gunicorn --bind=0.0.0.0:9501 config.wsgi --workers=5 --log-level=info --log-file=---access-logfile=- --error-logfile=- --timeout 30000 --reload
# exec gunicorn --bind=0.0.0.0:9091 config.wsgi --workers=5 --log-level=info --log-file=---access-logfile=- --error-logfile=- --timeout 30000 --reload