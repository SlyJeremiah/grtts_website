#!/usr/bin/env bash
set -o errexit

echo "=== Starting build process ==="

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input

echo "=== Checking superuser status ==="

# Use a multi-line Python script with a heredoc for clarity
python manage.py shell <<'EOF'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'shanyaslym19@gmail.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

print(f"Username from env: {username}")
print(f"Email from env: {email}")
print(f"Password set: {'Yes' if password else 'No'}")

if username and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superuser '{username}' created successfully!")
    else:
        print(f"✅ Superuser '{username}' already exists")
else:
    print("❌ Missing DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD environment variables")
EOF

echo "=== Superuser check complete ==="
echo "=== Build finished ==="
