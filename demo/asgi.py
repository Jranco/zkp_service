"""
ASGI config for zkp_service project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from FiatShamir.WebsocketConsumers.VerificationWSConsumer import VerificationWSConsumer
from FiatShamir.WebsocketConsumers.BindingWSConsumer import BindingWSConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        [
            # path("register/", YourWebSocketConsumer.as_asgi()),
            path("authenticate/", VerificationWSConsumer.as_asgi()),
            path("bindNewDevice/", BindingWSConsumer.as_asgi()),
        ]
    ),
})