#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files (these will go to whitenoise, not Cloudinary)
python manage.py collectstatic --no-input

# Create superuser if it doesn't exist (using environment variables)
echo "from django.contrib.auth import get_user_model; import os; User = get_user_model(); username = os.environ.get('DJANGO_SUPERUSER_USERNAME'); email = os.environ.get('DJANGO_SUPERUSER_EMAIL'); password = os.environ.get('DJANGO_SUPERUSER_PASSWORD'); if username and email and password: User.objects.filter(username=username).exists() or User.objects.create_superuser(username, email, password); print(f'Superuser {username} created or already exists.')" | python manage.py shell
