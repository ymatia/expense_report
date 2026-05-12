#!/bin/bash
set -e
curl -fsS "http://127.0.0.1:${APP_PORT:-8000}/health" > /dev/null
