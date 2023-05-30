#!/bin/bash
echo "PostgesSQL started"
python manage.py migrate
exec "$@"