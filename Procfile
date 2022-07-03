web: export DJANGO_SETTINGS_MODULE=project.settings_prod && gunicorn project.wsgi
release: python manage.py migrate --settings project.settings_prod
