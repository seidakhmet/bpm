import os
from datetime import datetime, date
from typing import Optional, List

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.common.mixins import models as mixins_models

from apps.tasks import (
    BusinessProcessStatuses,
    TaskColumnTypes,
    ExcelColumnIndex,
    parsers,
    TaskDelegationStatuses,
)
from apps.users import BPMGroups, models as users_models


User = get_user_model()


def get_excel_file_upload_path(instance, filename):
    return os.path.join("tasks", f"task_{str(instance.uuid)}", filename)


class BusinessProcess(mixins_models.TimestampModel, mixins_models.UUIDModel):
    """Модель бизнес-процесса"""

    id: int

    title: str = models.CharField(verbose_name=_("Title"), max_length=255)
    description: str = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    excel_file: models.FileField = models.FileField(upload_to=get_excel_file_upload_path, null=True, blank=True)
    dgd_code_column: int = models.IntegerField(
        verbose_name=_("DGD code column"),
        choices=ExcelColumnIndex.choices,
        default=ExcelColumnIndex.A,
    )
    dgd_name_column: int = models.IntegerField(
        verbose_name=_("DGD name column"),
        choices=ExcelColumnIndex.choices,
        default=ExcelColumnIndex.B,
    )
    ugd_code_column: int = models.IntegerField(
        verbose_name=_("UGD code column"),
        choices=ExcelColumnIndex.choices,
        default=ExcelColumnIndex.C,
        null=True,
        blank=True,
    )

    status: str = models.CharField(
        verbose_name=_("Status"),
        max_length=100,
        choices=BusinessProcessStatuses.choices,
        default=BusinessProcessStatuses.CREATED,
    )
    min_bpm_group: str = models.CharField(
        verbose_name=_("Min BPM group"),
        max_length=255,
        choices=BPMGroups.choices,
        default=BPMGroups.UGD_ISP,
        help_text=_("Minimum BPM group that can work with this business process"),
    )
    created_by_id: int
    created_by: User = models.ForeignKey(
        User, verbose_name=_("Created by"), on_delete=models.CASCADE, related_name="created_business_processes"
    )

    class Meta:
        verbose_name = _("Business process")
        verbose_name_plural = _("Business processes")

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, run_parser=True):
        super().save(force_insert, force_update, using, update_fields)
        if self.columns.count() == 0 and run_parser:
            self.parse()

    def parse(self):
        parser = parsers.ParserFactory.get_parser(self)
        parser.parse()


class TaskColumn(mixins_models.TimestampModel):
    """Модель колонки задачи"""

    id: int

    business_process_id: int
    business_process: BusinessProcess = models.ForeignKey(
        BusinessProcess, verbose_name=_("Task"), on_delete=models.CASCADE, related_name="columns"
    )

    column_index: int = models.IntegerField(verbose_name=_("Column index"), default=0)
    column_name: str = models.TextField(verbose_name=_("Column name"))
    column_type: str = models.CharField(
        verbose_name=_("Column type"), max_length=50, choices=TaskColumnTypes.choices, default=TaskColumnTypes.STRING
    )
    is_editable: bool = models.BooleanField(verbose_name=_("Is editable"), default=True)

    class Meta:
        verbose_name = _("Task column")
        verbose_name_plural = _("Task columns")

    def __str__(self):
        return f"{self.business_process}[{self.column_name}]"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        self.cells.update(column_index=self.column_index, column_type=self.column_type, is_editable=self.is_editable)


class TaskStatus(mixins_models.TimestampModel):
    """Модель статуса задачи"""

    id: int

    business_process_id: int
    business_process: BusinessProcess = models.ForeignKey(
        BusinessProcess, verbose_name=_("Business process"), on_delete=models.CASCADE, related_name="statuses"
    )

    status_name: str = models.CharField(verbose_name=_("Status name"), max_length=255)

    required_task_columns: models.ManyToManyField = models.ManyToManyField(
        TaskColumn, verbose_name=_("Required task columns"), related_name="required_statuses", blank=True
    )

    class Meta:
        verbose_name = _("Task status")
        verbose_name_plural = _("Task statuses")

    def __str__(self):
        return f"{self.business_process} [{self.status_name}]"


class Task(mixins_models.TimestampModel):
    """Модель задачи"""

    id: int

    business_process_id: int
    business_process: BusinessProcess = models.ForeignKey(
        BusinessProcess, verbose_name=_("Business process"), on_delete=models.CASCADE, related_name="tasks"
    )

    index: int = models.IntegerField(verbose_name=_("Index"), default=0)

    dgd_code: str = models.CharField(verbose_name=_("DGD code"), max_length=255, null=True, blank=True)
    dgd_code_number: str = models.CharField(verbose_name=_("DGD code number"), max_length=255, null=True, blank=True)
    dgd_name: str = models.CharField(verbose_name=_("DGD name"), max_length=255, null=True, blank=True)
    ugd_code: str = models.CharField(verbose_name=_("UGD code"), max_length=255, null=True, blank=True)

    status_id: int
    status: TaskStatus = models.ForeignKey(
        TaskStatus, verbose_name=_("Status"), on_delete=models.SET_NULL, related_name="tasks", null=True, blank=True
    )

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Task")

    def __str__(self):
        return f"{self.business_process}[{self.index}]"

    def get_cells(self):
        return [cell for cell in self.cells.all().order_by("column__column_index")]

    def get_last_delegation_instance(self, delegation_status: List[TaskDelegationStatuses] = None):
        instances = self.delegations.all()
        if delegation_status:
            instances = instances.filter(status__in=delegation_status)
        instances = instances.order_by("created_at")
        return instances.last() if instances else None

    def get_last_delegation_status(self):
        last_delegation = self.get_last_delegation_instance()
        return last_delegation.status if last_delegation else "no_delegation"

    def get_last_delegation(self):
        last_delegation = self.get_last_delegation_instance(
            delegation_status=[
                TaskDelegationStatuses.DELEGATED_TO_USER,
                TaskDelegationStatuses.SELF_DELEGATED,
                TaskDelegationStatuses.DELEGATED_TO_GROUP,
            ]
        )
        return last_delegation.delegated_to or last_delegation.delegated_to_bpm_group or _("No delegation")

    def get_current_executor(self):
        last_delegation = self.get_last_delegation_instance(
            delegation_status=[
                TaskDelegationStatuses.DELEGATED_TO_USER,
                TaskDelegationStatuses.SELF_DELEGATED,
            ]
        )
        return last_delegation.delegated_to or _("No executor")

    def get_user_last_delegation(self, user: User):
        last_delegation = (
            self.delegations.filter(
                Q(
                    delegated_to=user,
                    status__in=[
                        TaskDelegationStatuses.DELEGATED_TO_USER,
                        TaskDelegationStatuses.SENT_TO_REWORK,
                    ],
                )
                | Q(
                    delegated_to_bpm_group__in=user.bpm_groups.all(),
                    status=TaskDelegationStatuses.DELEGATED_TO_GROUP,
                ),
            )
            .order_by("created_at")
            .last()
        )
        return last_delegation

    def get_last_approve_delegation(self):
        last_delegation = (
            self.delegations.filter(
                status=TaskDelegationStatuses.SENT_TO_APPROVAL,
            )
            .order_by("created_at")
            .last()
        )
        return last_delegation

    def get_current_worker(self):
        last_delegation = self.get_last_delegation_instance()
        return last_delegation.delegated_to or _("No worker")

    def is_delegated_to_user(self):
        last_delegation = self.get_last_delegation_instance()
        return last_delegation and last_delegation.status == TaskDelegationStatuses.DELEGATED_TO_USER

    def is_delegated_to_group(self):
        last_delegation = self.get_last_delegation_instance()
        return last_delegation and last_delegation.status == TaskDelegationStatuses.DELEGATED_TO_GROUP

    def is_self_delegated(self):
        last_delegation = self.get_last_delegation_instance()
        return last_delegation and last_delegation.status == TaskDelegationStatuses.SELF_DELEGATED

    def is_returned_to_delegator(self):
        last_delegation = self.get_last_delegation_instance()
        return last_delegation and last_delegation.status == TaskDelegationStatuses.RETURNED_TO_DELEGATOR

    def is_sent_to_approval(self):
        last_delegation = self.get_last_delegation_instance()
        return last_delegation and last_delegation.status == TaskDelegationStatuses.SENT_TO_APPROVAL

    def is_sent_to_rework(self):
        last_delegation = self.get_last_delegation_instance()
        return last_delegation and last_delegation.status == TaskDelegationStatuses.SENT_TO_REWORK

    def get_delegation_history(self):
        return self.delegations.all().order_by("created_at")

    @property
    def get_status(self):
        return self.status.status_name if self.status else ""


class TaskCell(mixins_models.TimestampModel):
    """Модель ячейки задачи"""

    id: int

    business_process_id: int
    business_process: BusinessProcess = models.ForeignKey(
        BusinessProcess, verbose_name=_("Business process"), on_delete=models.CASCADE, related_name="cells"
    )

    column_id: int
    column: TaskColumn = models.ForeignKey(
        TaskColumn, verbose_name=_("Task column"), on_delete=models.CASCADE, related_name="cells"
    )

    task_id: int
    task: Task = models.ForeignKey(Task, verbose_name=_("Task"), on_delete=models.CASCADE, related_name="cells")

    value: str = models.TextField(verbose_name=_("Value"), null=True, blank=True)

    column_index: int = models.IntegerField(verbose_name=_("Column index"), default=0)
    column_type: str = models.CharField(
        verbose_name=_("Column type"), max_length=50, choices=TaskColumnTypes.choices, default=TaskColumnTypes.STRING
    )
    is_editable: bool = models.BooleanField(verbose_name=_("Is editable"), default=True)

    class Meta:
        verbose_name = _("Task cell")
        verbose_name_plural = _("Task cells")
        ordering = ("id",)

    @property
    def get_template_value(self):
        return self.value

    @property
    def get_initial_value(self):
        return self._initial_value

    def __str__(self):
        return f"{self.business_process}[{self.column.column_index}, {self.task.index}] - {self.value}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_value = self.value

    def input_type(self):
        if self.column_type == TaskColumnTypes.STRING:
            return "text"
        elif self.column_type == TaskColumnTypes.TEXT:
            return "textarea"
        elif self.column_type == TaskColumnTypes.INTEGER:
            return "number"
        elif self.column_type == TaskColumnTypes.FLOAT:
            return "number"
        elif self.column_type == TaskColumnTypes.DATE:
            return "date"
        elif self.column_type == TaskColumnTypes.DATE_TIME:
            return "datetime-local"
        elif self.column_type == TaskColumnTypes.BOOLEAN:
            return "checkbox"
        return "text"

    def is_boolean(self):
        return self.column_type == TaskColumnTypes.BOOLEAN

    def is_text(self):
        return self.column_type == TaskColumnTypes.TEXT


class TaskCellValueLog(mixins_models.TimestampModel):
    """Модель лога ячейки задачи"""

    id: int

    task_cell_id: int
    task_cell: TaskCell = models.ForeignKey(
        TaskCell, verbose_name=_("Task cell"), on_delete=models.CASCADE, related_name="logs"
    )

    old_value: str = models.TextField(verbose_name=_("Old value"), null=True, blank=True)
    new_value: str = models.TextField(verbose_name=_("New value"), null=True, blank=True)

    created_by_id: int
    created_by: User = models.ForeignKey(
        User, verbose_name=_("Created by"), on_delete=models.CASCADE, related_name="created_task_cell_values"
    )

    class Meta:
        verbose_name = _("Task cell value log")
        verbose_name_plural = _("Task cell value logs")

    def __str__(self):
        return f"{self.task_cell}[{self.old_value}, {self.new_value}]"


class TaskComment(mixins_models.TimestampModel):
    """Модель комментария задачи"""

    id: int

    task_id: int
    task: Task = models.ForeignKey(Task, verbose_name=_("Task"), on_delete=models.CASCADE, related_name="comments")

    text: str = models.TextField(verbose_name=_("Text"))

    created_by_id: int
    created_by: User = models.ForeignKey(
        User, verbose_name=_("Created by"), on_delete=models.CASCADE, related_name="created_task_comments"
    )

    class Meta:
        verbose_name = _("Task comment")
        verbose_name_plural = _("Task comments")

    def __str__(self):
        return f"{self.task}[{self.text}]"


class TaskDelegation(mixins_models.TimestampModel):
    """Модель делегирования задачи"""

    id: int

    task_id: int
    task: Task = models.ForeignKey(Task, verbose_name=_("Task"), on_delete=models.CASCADE, related_name="delegations")

    status: str = models.CharField(
        verbose_name=_("Status"),
        max_length=100,
        choices=TaskDelegationStatuses.choices,
        default=TaskDelegationStatuses.DELEGATED_TO_USER,
    )

    delegated_to_bpm_group_id: int
    delegated_to_bpm_group: str = models.ForeignKey(
        users_models.BPMGroup,
        verbose_name=_("Delegated to group"),
        on_delete=models.SET_NULL,
        related_name="delegated_task_delegations",
        null=True,
        blank=True,
    )

    delegated_to_id: int
    delegated_to: User = models.ForeignKey(
        User,
        verbose_name=_("Delegated to"),
        on_delete=models.CASCADE,
        related_name="delegated_task_delegations",
        null=True,
        blank=True,
    )

    created_by_id: int
    created_by: User = models.ForeignKey(
        User, verbose_name=_("Created by"), on_delete=models.CASCADE, related_name="created_task_delegations"
    )

    class Meta:
        verbose_name = _("Task delegation")
        verbose_name_plural = _("Task delegations")

    def __str__(self):
        return f"{self.task}[{self.status}]"
