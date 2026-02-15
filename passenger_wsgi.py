# passenger_wsgi.py
import os
import sys

# Add your project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'grtts_project.settings'

# Import and return the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()