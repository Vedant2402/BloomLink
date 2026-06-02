"""
ASGI config for BHome project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

# Ensure Django settings are set before importing Django-dependent modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BHome.settings')

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# initialize Django ASGI application first so apps are ready
django_asgi_app = get_asgi_application()

from chatapp.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})
