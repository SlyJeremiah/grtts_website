"""
WSGI config for grtts_project project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grtts_project.settings')

application = get_wsgi_application()

# Vercel looks for 'app' – so we create an alias
app = application