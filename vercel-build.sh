#!/bin/bash
echo "=== Running Vercel Build ==="
python manage.py collectstatic --no-input
echo "=== Build Complete ==="
