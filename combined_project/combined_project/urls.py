from django.contrib import admin
from django.urls import path
from books.api_ninja import api as ninja_api
from books import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", ninja_api.urls),       # Django Ninja endpoints under /api/
    path("", views.ninja_page, name="ninja_home"),
    path("fastapi/", views.fastapi_page, name="fastapi_home"),
]
