from django.urls import path, include

urlpatterns = [
    path("v1/token/", include("apps.api.urls.token")),
    path("v1/tasks/", include("apps.api.urls.tasks")),
]
