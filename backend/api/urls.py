from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
routes = [
    ("spy_cat", views.SpyCatView),
]


for route, view in routes:
    router.register(route, view)


urlpatterns = [
    path("", include(router.urls)),
]