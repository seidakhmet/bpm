from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View

from apps.tasks.models import Task


class TaskView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task_rows = task.rows.all()
        rows = [row.get_cells() for row in task_rows.order_by("id").prefetch_related("cells")]

        return render(
            request,
            "web/pages/task_detail.html",
            {
                "task": task,
                "is_owner": task.created_by == request.user,
                "columns": task.columns.all().order_by("id"),
                "rows": rows,
            },
        )
