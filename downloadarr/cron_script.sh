#!/bin/bash

# Function to change ownership recursively
change_ownership() {
    chown -R "$1:$2" /app
}
change_ownership "$PUID" "$PGID"

# Path to the lock file
LOCK_FILE="/tmp/cron_script.lock"

# Check if lock file exists
if [ -e "$LOCK_FILE" ]; then
    echo "Script is already running, exiting."
    exit 1
fi

# Create lock file
touch "$LOCK_FILE"

# Run the main.py script
python /app/main.py

# Remove lock file when script completes
rm -f "$LOCK_FILE"
