#!/bin/bash

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
exec su-exec "$UID:$GID" python /app/main.py

# Remove lock file when script completes
rm -f "$LOCK_FILE"
