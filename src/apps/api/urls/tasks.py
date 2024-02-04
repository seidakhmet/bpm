from django.urls import path, include
from rest_framework import routers

from apps.api.viewsets import BusinessProcessViewSet

router = routers.DefaultRouter()


router.register("business-process", BusinessProcessViewSet, basename="business-process")


urlpatterns = [
    path("", include(router.urls)),
]
