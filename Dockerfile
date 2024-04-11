# Use Alpine Linux as base
FROM python:3.9-alpine

# Install required packages
RUN apk add --no-cache \
    ffmpeg

# Set working directory
WORKDIR /app

# Create config directory
RUN mkdir /config

# Copy the Python project from GitHub
ARG GITHUB_REPO=https://github.com/riffsphereha/downloadarr.git
RUN apk add --no-cache git && \
    git clone --single-branch --depth 1 --branch main $GITHUB_REPO /tmp/downloadarr && \
    mv /tmp/downloadarr/downloadarr/* ./ && \
    rm -rf /tmp/downloadarr

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Cleanup unnecessary files
RUN rm -rf /var/cache/apk/*

# Copy example config file into config directory
RUN wget -O /config/example_config.yml https://github.com/riffsphereha/downloadarr/tree/main/config/config.yml

# Add script to update crontab dynamically
RUN chmod +x update_crontab.sh

# Run script to update crontab during container startup
CMD ["/bin/sh", "-c", "/app/update_crontab.sh && crond -f"]
