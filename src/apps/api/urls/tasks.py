from django.urls import path, include
from rest_framework import routers

from apps.api.viewsets import BusinessProcessViewSet, TaskCommentViewSet, TaskViewSet

router = routers.DefaultRouter()


router.register("business-process", BusinessProcessViewSet, basename="business-process")
router.register("task-comment", TaskCommentViewSet, basename="task-comment")
router.register("task", TaskViewSet, basename="task")


urlpatterns = [
    path("", include(router.urls)),
]
