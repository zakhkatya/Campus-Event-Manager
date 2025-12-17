# Campus Event Manager 🎓

## Make Migrations when changing Models
``` sh
docker compose exec ems_web python manage.py makemigrations
```

## Collect static files after upload
``` sh
docker compose exec ems_web python manage.py collectstatic --no-input
```

## Insert dummy data in database
``` sh
docker compose exec ems_web python manage.py seed_big_dummy_data 
```