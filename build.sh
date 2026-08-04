#!/usr/bin/env bash
# Vercel build step: install deps, collect static files, and run migrations.
set -o errexit

# Install Python dependencies for the build environment.
python3 -m pip install -r requirements.txt

# Collect static files into STATIC_ROOT (staticfiles_build/static),
# which Vercel serves from its CDN (see vercel.json).
python3 manage.py collectstatic --noinput --clear

# Apply database migrations. In production this targets the PostgreSQL
# database referenced by DATABASE_URL; locally it is a no-op against SQLite.
python3 manage.py migrate --noinput
