#!/bin/bash
set -e

echo "Waiting for Postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "Postgres is up!"

# Optional: Run DB migrations here (if any)
# python scripts/run_migrations.py

echo "Starting API with Gunicorn..."
exec gunicorn \
    -c /app/docker/gunicorn.conf.py \
    api.main:app
