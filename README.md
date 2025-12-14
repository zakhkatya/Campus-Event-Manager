# Campus Event Manager 🎓

## Make Migrations when changing Models
``` sh
docker compose exec ems_web python manage.py makemigrations
```

## Collect static files after upload
``` sh
docker compose exec ems_web python manage.py collectstatic --no-input
```