#!/bin/bash
set -e
# Use /heartbeat — AppAPIAuthMiddleware always exempts it (unlike /health).
curl -fsS "http://127.0.0.1:${APP_PORT:-8000}/heartbeat" > /dev/null
