#!/bin/bash
set -e

echo "🔄 Running database migrations..."
uv run python manage.py migrate

echo "🔄 Collecting static files..."
uv run python manage.py collectstatic --noinput

echo "🚀 Starting Django server..."
exec "$@"
