#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
python -m gunicorn core.wsgi:application \
    --bind 0.0.0.0:80 \
    -w 4 \
    --chdir . \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    -t 60 \
    --reload
