from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.tasks.models import (
    BusinessProcess,
    TaskColumn,
    Task,
    TaskCell,
    TaskCellValueLog,
    TaskStatus,
    TaskComment,
    TaskDelegation,
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
    list_display = (
        "business_process",
        "column_name",
        "task_index",
        "old_value",
        "new_value",
        "created_by",
        "created_at_pretty",
    )
    ordering = ("-created_at",)

    def business_process(self, obj):
        return obj.task_cell.business_process

    business_process.short_description = _("Business process")

    def task_index(self, obj):
        return obj.task_cell.task.index

    task_index.short_description = _("Task index")

    def column_name(self, obj):
        return obj.task_cell.column.column_name

    column_name.short_description = _("Column name")


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskDelegation)
class TaskDelegationAdmin(admin.ModelAdmin):
    list_display = [
        "task",
        "status",
        "delegated_to_bpm_group",
        "delegated_to",
        "created_by",
    ]
    search_fields = [
        "task__business_process__title",
        "delegated_to_bpm_group__bpm_group_name",
        "delegated_to__bpm_full_name",
        "delegated_to__first_name",
        "delegated_to__last_name",
        "created_by__bpm_full_name",
        "created_by__first_name",
        "created_by__last_name",
        "task__cells__value",
    ]
    list_filter = ["status"]
