#!/bin/bash
# Démarrer Redis en arrière-plan
redis-server --daemonize yes

# Attendre que la base de données soit prête
python manage.py wait_for_db

# Exécuter les migrations
python manage.py makemigrations
python manage.py migrate

# Démarrer Gunicorn avec Uvicorn
exec gunicorn project.asgi:application -k uvicorn.workers.UvicornWorker -c gunicorn_config.py
