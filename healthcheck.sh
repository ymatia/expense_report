#!/bin/bash
# Match Nextcloud Python ExApp skeleton: with HaRP, frpc must be running.
# Without HaRP, probe /heartbeat over TCP (nc_py_api exempts it from AppAPI auth).

set -e

if [ -f /frpc.toml ] && [ -n "$HP_SHARED_KEY" ]; then
  if pgrep -x "frpc" > /dev/null; then
    exit 0
  else
    exit 1
  fi
fi

curl -fsS "http://127.0.0.1:${APP_PORT:-8000}/heartbeat" > /dev/null
