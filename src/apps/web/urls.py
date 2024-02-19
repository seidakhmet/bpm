from django.urls import path, include

from apps.web.views import (
    IndexView,
    LoginView,
    AddBusinessProcessView,
    DetailBusinessProcessView,
    EditBusinessProcessView,
    DeleteBusinessProcessView,
    EditBusinessProcessColumnView,
    StatusDetailBusinessProcessView,
    AddTaskStatusView,
    EditTaskStatusView,
    DeleteTaskStatusView,
    TaskView,
    GroupTaskView,
    DelegatedTaskView,
    PublishBusinessProcessView,
    ApproveTaskView,
)

urlpatterns = [
    path("task/<int:pk>/", TaskView.as_view(), name="task"),
    path("", IndexView.as_view(), name="index"),
    path("business-process/add/", AddBusinessProcessView.as_view(), name="add-business-process"),
    path("business-process/<int:pk>/", DetailBusinessProcessView.as_view(), name="detail-business-process"),
    path(
        "business-process/<int:pk>/statuses/",
        StatusDetailBusinessProcessView.as_view(),
        name="status-detail-business-process",
    ),
    path(
        "business-process/<int:pk>/tasks/",
        TaskView.as_view(),
        name="tasks-business-process",
    ),
    path(
        "business-process/<int:pk>/group-tasks/",
        GroupTaskView.as_view(),
        name="group-tasks-business-process",
    ),
    path(
        "business-process/<int:pk>/delegated-tasks/",
        DelegatedTaskView.as_view(),
        name="delegated-tasks-business-process",
    ),
    path(
        "business-process/<int:pk>/approve-tasks/",
        ApproveTaskView.as_view(),
        name="approve-tasks-business-process",
    ),
    path(
        "business-process/<int:pk>/statuses/add/",
        AddTaskStatusView.as_view(),
        name="add-status-business-process",
    ),
    path(
        "business-process/statuses/<int:pk>/edit/",
        EditTaskStatusView.as_view(),
        name="edit-status-business-process",
    ),
    path(
        "business-process/statuses/<int:pk>/publish/",
        PublishBusinessProcessView.as_view(),
        name="publish-status-business-process",
    ),
    path(
        "business-process/statuses/<int:pk>/delete/",
        DeleteTaskStatusView.as_view(),
        name="delete-status-business-process",
    ),
    path("business-process/<int:pk>/edit/", EditBusinessProcessView.as_view(), name="edit-business-process"),
    path("business-process/<int:pk>/delete/", DeleteBusinessProcessView.as_view(), name="delete-business-process"),
    path(
        "business-process/<int:pk>/columns/",
        EditBusinessProcessColumnView.as_view(),
        name="edit-business-process-columns",
    ),
    path("login/<uuid:token>/", LoginView.as_view(), name="login"),
]
