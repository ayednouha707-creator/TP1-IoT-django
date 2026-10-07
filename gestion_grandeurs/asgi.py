"""
ASGI config for gestion_grandeurs project.
Interface avec le web asynchrone (Django Channels + Daphne).
"""
import os

import django
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_grandeurs.settings')

django.setup()

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
})
