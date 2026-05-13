#!/bin/bash
set -e

echo "=== Starting Vercel Build ==="

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --no-input

# Collect static files (this is critical for admin CSS)
echo "=== Collecting static files ==="
python manage.py collectstatic --no-input --clear

# Show what was collected
echo "=== Static files collected ==="
ls -la staticfiles/admin/css/ | head -20

echo "=== Build Complete ==="
