"""Vercel build script for AgroNity.

Runs automatically during each Vercel deploy (configured via the
`buildCommand` in vercel.json). It uses the same Python interpreter Vercel
installed the dependencies into, so there is no pip/uv step here.

Steps:
1. collectstatic  - gather static files (also run automatically by Vercel;
   kept here as a safe no-op-ish belt-and-suspenders).
2. migrate        - create/upgrade database tables. In production this targets
   the PostgreSQL database from DATABASE_URL; with no DATABASE_URL it is a
   harmless no-op against a throwaway SQLite file.
3. createsuperuser (optional) - only if DJANGO_SUPERUSER_USERNAME and
   DJANGO_SUPERUSER_PASSWORD are set. Idempotent: ignored if the user exists.
"""

import os
import subprocess
import sys


def run(*args):
    subprocess.run([sys.executable, "manage.py", *args], check=True)


def main():
    run("collectstatic", "--noinput")
    run("migrate", "--noinput")

    if os.environ.get("DJANGO_SUPERUSER_USERNAME") and os.environ.get("DJANGO_SUPERUSER_PASSWORD"):
        try:
            run("createsuperuser", "--noinput")
            print("Superuser created from environment variables.")
        except subprocess.CalledProcessError:
            # Superuser already exists (or username taken) — safe to ignore.
            print("Superuser already exists; skipping creation.")


if __name__ == "__main__":
    main()
