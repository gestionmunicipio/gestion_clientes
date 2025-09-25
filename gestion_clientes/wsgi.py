"""
WSGI config for gestion_clientes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys

# Agrega la ruta de tu proyecto
path = '/home/gestionmunicipio/cliente_admin'  # ← AJUSTA con tu usuario
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cliente_admin.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
