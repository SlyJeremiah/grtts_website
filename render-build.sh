#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files (these will go to whitenoise, not Cloudinary)
python manage.py collectstatic --no-input