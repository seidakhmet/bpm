from django.urls import path, include
from rest_framework import routers

from apps.api.viewsets import TokenRequestViewSet

router = routers.DefaultRouter()

router.register("token", TokenRequestViewSet, basename="token")

urlpatterns = [
    path("", include(router.urls)),
]
