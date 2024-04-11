#!/bin/sh

# Create config file if not exits
CONFIG_FILE="/config/config.yml"
EXAMPLE_CONFIG_FILE="/app/config.yml"

# Check if the config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    # If the config file doesn't exist, copy it from the example config
    cp "$EXAMPLE_CONFIG_FILE" "$CONFIG_FILE"
    echo "Config file copied successfully."
else
    echo "Config file already exists."
fi

# Set the cron schedule from the CRON_SCHEDULE environment variable
CRON_SCHEDULE=${CRON_SCHEDULE:-"0 * * * *"}
UUID=${UUID:-99}
GUID=${GUID:-100}

# Write the cron schedule and command to a temporary file
echo "$CRON_SCHEDULE sh /app/cron_script.sh" > /etc/crontabs/root

# Load the new crontab configuration
crontab /etc/crontabs/root