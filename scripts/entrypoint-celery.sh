#!/bin/bash
set -e

mkdir -p /app/logs

echo "🚀 Starting Celery worker..."
exec "$@"
