# Simple Social Network

A Django project for a basic social-networking application, organized into account, home, and social apps with Django templates.

## Repository layout
- `account/` — account-related functionality
- `home/` — homepage/views
- `social/` — social-network features
- `templates/` — server-rendered pages
- `manage.py` — Django management entry point

## Run locally
Requires Python and pip.

```bash
git clone https://github.com/behrouzyou/simple-social-network.git
cd simple-social-network
python -m venv .venv
```

Activate the environment and install the dependencies required by the project. Configure a private development secret key, then run:

```bash
python manage.py migrate
python manage.py runserver
```

## Notes
This README describes the repository layout at a high level. Check the app views, models, and URL configurations for the exact feature set and install dependencies based on the project's imports.
