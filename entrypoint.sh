#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

chmod +x /app/crons_config.sh
sh /app/crons_config.sh

# Start Gunicorn server
echo "Starting Gunicorn server..."
cron && gunicorn --bind 0.0.0.0:8000 raad_panel.wsgi:application
