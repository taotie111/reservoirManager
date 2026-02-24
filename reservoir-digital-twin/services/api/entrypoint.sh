#!/bin/sh
set -e
echo "Applying Alembic migrations..."
alembic upgrade head || true
echo "Seeding initial data..."
python -m reservoir_digital_twin_seed_setup || true
echo "Starting API..."
exec "$@"
