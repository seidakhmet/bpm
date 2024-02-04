from django.urls import path, include

urlpatterns = [
    path("api/", include("apps.api.urls")),
    path("", include("apps.web.urls")),
]
