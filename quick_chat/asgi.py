"""
ASGI config for quick_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quick_chat.settings')
import django
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns

# from django.core.asgi import get_asgi_application



application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
