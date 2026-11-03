import os
import sys
import asyncio
import django

# Fix Windows: mqttasgi a besoin du "selector" event loop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_grandeurs.settings')
django.setup()

# ⚠️ ces imports doivent rester APRÈS django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

from mqtt_topics.consumers import GrandeurMqttConsumer
from dashboard.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'mqtt': GrandeurMqttConsumer.as_asgi(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    ),
})