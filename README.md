# Simple Social Network

A Django project for a basic social-networking application, organized into account, home, and social apps with Django templates.

## Structure
- `account/` — account-related functionality
- `home/` — homepage/views
- `social/` — social-network features
- `templates/` — server-rendered pages
- `manage.py` — Django management entry point

## Run locally
Create and activate a Python virtual environment, install the dependencies required by the project, configure a private development secret key, and run:

```bash
python manage.py migrate
python manage.py runserver
```

Check the app views, models, and URL configurations for the exact feature set and dependencies.
