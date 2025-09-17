"""
ASGI config for combined Django + FastAPI project.
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from books.api_fastapi import app as fastapi_app
from django.urls import path
from django.http import HttpResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "combined_project.settings")

django_asgi_app = get_asgi_application()

# Optional: CORS for FastAPI
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your Django domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from starlette.middleware.wsgi import WSGIMiddleware
from starlette.routing import Mount, Route
from starlette.applications import Starlette

# Combine Django and FastAPI
application = Starlette(routes=[
    Mount("/FastApi", app=fastapi_app),
    Mount("/", app=WSGIMiddleware(django_asgi_app)),
])
