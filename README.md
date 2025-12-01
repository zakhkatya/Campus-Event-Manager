## This file created for explaining project and show commands
# How To Create Virtual Environment And Activate It
```bash 
python -m venv .venv
.venv\Scripts\activate
```

# How To Install Necessary Packages For Development Environment
```bash
pip install -r Docker/requirements.txt
```

# How To Launch Environment 
```bash
docker-compose up --build -d
```
# How To Create Project And Application
```bash
django-admin startproject ems .
python manage.py startapp event_system
```
# How To Create A Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```
