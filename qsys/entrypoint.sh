#!/bin/bash

# Generate static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Auto setup
python manage.py autosetup

# Set write permission
chmod 666 db.sqlite3

# Start server
uwsgi --ini uwsgi.ini --enable-threads
