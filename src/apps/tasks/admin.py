from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.tasks.models import (
    BusinessProcess,
    TaskColumn,
    Task,
    TaskCell,
    TaskCellValueLog,
)


@admin.register(BusinessProcess)
class BusinessProcessAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskColumn)
class TaskColumnAdmin(admin.ModelAdmin):
    list_display = (
        "business_process",
        "column_index",
        "column_name",
        "column_type",
        "is_editable",
    )
    ordering = ("business_process", "column_index")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "business_process",
        "index",
        "dgd_code",
        "dgd_name",
        "ugd_code",
    )
    ordering = ("business_process", "index")


@admin.register(TaskCell)
class TaskCellAdmin(admin.ModelAdmin):
    list_display = (
        "business_process",
        "column_name",
        "task_index",
        "value",
    )
    ordering = ("business_process", "task", "column")

    def task_index(self, obj):
        return obj.task.index

    task_index.short_description = _("Task index")

    def column_name(self, obj):
        return obj.column.column_name

    column_name.short_description = _("Column name")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        TaskCellValueLog.objects.create(
            created_by=request.user,
            task_cell=obj,
            old_value=obj.get_initial_value,
            new_value=obj.value,
        )


@admin.register(TaskCellValueLog)
class TaskCellValueLogAdmin(admin.ModelAdmin):
    pass
