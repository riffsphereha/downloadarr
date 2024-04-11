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
    mv /tmp/downloadarr/* ./ && \
    rm -rf /tmp/downloadarr

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Cleanup unnecessary files
RUN rm -rf /var/cache/apk/*

# Copy example config file into config directory
RUN wget -O /config/example_config.yml https://github.com/riffsphereha/downloadarr/tree/main/config/config.yml

# Set up cron schedule from environmental variable
ENV CRON_SCHEDULE="0 * * * *"
RUN echo "$CRON_SCHEDULE /app/cron_script.sh" > /etc/crontabs/root

# Run cron in foreground
CMD ["crond", "-f"]
