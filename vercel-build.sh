#!/bin/bash
set -euo pipefail

echo "=== GRTTS build ==="

pip install -r requirements.txt

# Applies any unapplied migrations. Migrations are additive by design — review
# every generated migration before merging; this runs automatically on deploy.
echo "=== Applying migrations ==="
python manage.py migrate --no-input

# static/ is committed and served by Vercel's CDN. collectstatic only populates
# staticfiles/ for WhiteNoise as a fallback; --clear is deliberately not used.
echo "=== Collecting static files ==="
python manage.py collectstatic --no-input

echo "=== Build complete ==="
