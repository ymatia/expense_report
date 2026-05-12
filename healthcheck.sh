#!/bin/sh
set -e
# When HP_SHARED_KEY is set, nc_py_api run_app() listens on a Unix socket only (no TCP).
# Otherwise it binds to APP_HOST:APP_PORT.
# /heartbeat is always exempt from AppAPIAuthMiddleware.
if [ -n "$HP_SHARED_KEY" ]; then
  SOCK="${HP_EXAPP_SOCK:-/tmp/exapp.sock}"
  curl -fsS --unix-socket "$SOCK" "http://localhost/heartbeat" > /dev/null
else
  curl -fsS "http://127.0.0.1:${APP_PORT:-8000}/heartbeat" > /dev/null
fi
