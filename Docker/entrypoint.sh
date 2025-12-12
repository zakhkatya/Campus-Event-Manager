#!/bin/bash

if [ ! -d "node_modules" ]; then
  npm install
  npm i bootstrap-icons
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000