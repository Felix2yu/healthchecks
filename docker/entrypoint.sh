#!/bin/bash
set -e

DATA_DIR="/data"
if [ -d "/config" ]; then
    DATA_DIR="/config"
fi

mkdir -p "$DATA_DIR"
chown hc:hc "$DATA_DIR"

if [ -z "$SECRET_KEY" ]; then
    KEY_FILE="$DATA_DIR/SECRET_KEY"
    if [ ! -f "$KEY_FILE" ]; then
        python3 -c "import secrets; print(secrets.token_urlsafe(32))" > "$KEY_FILE"
        chown hc:hc "$KEY_FILE"
    fi
    export SECRET_KEY
    SECRET_KEY=$(cat "$KEY_FILE")
fi

LS_FILE="$DATA_DIR/local_settings.py"
if [ -f "$LS_FILE" ] && [ ! -f /opt/healthchecks/hc/local_settings.py ]; then
    ln -sf "$LS_FILE" /opt/healthchecks/hc/local_settings.py
fi

exec su -s /bin/bash hc -c "exec $*"
