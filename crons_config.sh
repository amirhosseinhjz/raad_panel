# Create a file for the cron job
touch /etc/cron.d/cron_job

# Add the cron job to the cron file
echo "*/1 * * * * root cd /app/ && /usr/local/bin/python manage.py runcrons >> /var/log/cron.log 2>&1" > /etc/cron.d/cron_job

# Give execution rights on the cron job
chmod 0644 /etc/cron.d/cron_job

# Apply cron job
crontab /etc/cron.d/cron_job

# Create the log file to be able to run tail
touch /var/log/cron.log
