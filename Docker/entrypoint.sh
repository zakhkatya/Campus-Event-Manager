#!/bin/bash

echo "Checking for frontend dependencies..."
if [ ! -d "node_modules" ]; then
    npm install
fi

echo "Running migrations and collectstatic..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Starting debug server on 0.0.0.0:8000 (debug port: 5678)"
echo "Waiting for debugger to attach..."

python -Xfrozen_modules=off -m debugpy --wait-for-client --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000 --noreload