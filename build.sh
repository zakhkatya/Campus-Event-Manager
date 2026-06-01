#!/usr/bin/env bash
set -o errexit

pip install -r docker/requirements.txt

cd ems
npm install
python manage.py compilescss
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py seed_big_dummy_data