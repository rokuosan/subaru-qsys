#!/bin/bash

# Generate static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Start server
uwsgi --ini uwsgi.ini --enable-threads
