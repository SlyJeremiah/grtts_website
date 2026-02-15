#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "=== Starting build process ==="

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# ============================================
# SUPERUSER CREATION WITH VERBOSE OUTPUT
# ============================================
echo "=== Checking superuser status ==="

# Create a Python script to handle superuser creation
python << END
import os
import django
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grtts_project.settings')
django.setup()

User = get_user_model()

# Get credentials from environment variables
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'shanyaslym19@gmail.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

print(f"Username from env: {username}")
print(f"Email from env: {email}")
print(f"Password set: {'Yes' if password else 'No'}")

if not username or not password:
    print("❌ ERROR: Username or password not set in environment variables")
    print("Please set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD")
    exit(1)

# Check if user exists
user_exists = User.objects.filter(username=username).exists()
print(f"User '{username}' exists: {user_exists}")

if not user_exists:
    try:
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superuser '{username}' created successfully!")
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        exit(1)
else:
    print(f"✅ Superuser '{username}' already exists")
END

echo "=== Superuser check complete ==="
echo "=== Build finished ==="
