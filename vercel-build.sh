#!/bin/bash
set -e
echo "=== VERCEL BUILD START ==="
echo "Current directory: $(pwd)"

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Running collectstatic ==="
python manage.py collectstatic --no-input --clear

echo "=== CHECKING GENERATED FILES ==="
echo "Staticfiles directory contents:"
ls -la staticfiles/
echo -e "\nCSS directory contents (with hashes):"
ls -la staticfiles/css/ || echo "No css directory"
echo -e "\nImages directory contents (with hashes):"
ls -la staticfiles/images/ || echo "No images directory"

echo -e "\n=== FIRST 10 LINES OF MANIFEST ==="
if [ -f staticfiles/staticfiles.json ]; then
    head -20 staticfiles/staticfiles.json
else
    echo "❌ No manifest file found!"
fi

echo "=== Build complete ==="
