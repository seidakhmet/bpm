from django.urls import path, include

from apps.web.views import (
    IndexView,
    LoginView,
    TaskView,
    AddBusinessProcessView,
    DetailBusinessProcessView,
    EditBusinessProcessView,
    DeleteBusinessProcessView,
    EditBusinessProcessColumnView,
)

urlpatterns = [
    path("task/<int:pk>/", TaskView.as_view(), name="task"),
    path("", IndexView.as_view(), name="index"),
    path("business-process/add/", AddBusinessProcessView.as_view(), name="add-business-process"),
    path("business-process/<int:pk>/", DetailBusinessProcessView.as_view(), name="detail-business-process"),
    path("business-process/<int:pk>/edit/", EditBusinessProcessView.as_view(), name="edit-business-process"),
    path("business-process/<int:pk>/delete/", DeleteBusinessProcessView.as_view(), name="delete-business-process"),
    path(
        "business-process/<int:pk>/columns/",
        EditBusinessProcessColumnView.as_view(),
        name="edit-business-process-columns",
    ),
    path("login/<uuid:token>/", LoginView.as_view(), name="login"),
]
