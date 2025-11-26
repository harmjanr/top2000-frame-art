#!/usr/bin/with-contenv bashio

# Read configuration from Home Assistant
export TV_IP=$(bashio::config 'tv_ip')
export CHECK_INTERVAL=$(bashio::config 'check_interval')
export LASTFM_API_KEY=$(bashio::config 'lastfm_api_key')

bashio::log.info "Starting Top 2000 Frame Art addon..."
bashio::log.info "TV IP: ${TV_IP}"
bashio::log.info "Check Interval: ${CHECK_INTERVAL} seconds"

# Run the Python application
python3 /app/app.py
