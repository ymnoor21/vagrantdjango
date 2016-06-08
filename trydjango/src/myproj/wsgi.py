"""
WSGI config for myproj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

EXTRA_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..')) + '/src'
if EXTRA_DIR not in sys.path:
    sys.path.append(EXTRA_DIR)

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproj.settings")

application = get_wsgi_application()
