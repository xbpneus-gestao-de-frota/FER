"""
WSGI config for XBPNEUS Premium project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbpneus.config.settings')

application = get_wsgi_application()

