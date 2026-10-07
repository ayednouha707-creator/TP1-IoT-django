"""
ASGI config for gestion_grandeurs project.
Protocoles gérés : http (Daphne) et mqtt (mqttasgi).
"""
import os

import django
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_grandeurs.settings')

django.setup()

from mqtt_topics.consumers import MyMqttConsumer  # noqa: E402 (après django.setup())

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'mqtt': MyMqttConsumer.as_asgi(),
})
