#!/bin/sh

# Set the cron schedule from the CRON_SCHEDULE environment variable
CRON_SCHEDULE=${CRON_SCHEDULE:-"0 * * * *"}

# Write the cron schedule and command to a temporary file
echo "$CRON_SCHEDULE /app/cron_script.sh" > /etc/crontabs/root

# Load the new crontab configuration
crontab /etc/crontabs/root