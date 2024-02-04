import os
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.mixins import models as mixins_models

from apps.tasks import (
    BusinessProcessStatuses,
    TaskColumnTypes,
    ExcelColumnIndex,
    parsers,
)
from apps.users import BPMGroups


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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.excel_file:
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

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Task")

    def __str__(self):
        return f"{self.business_process}[{self.index}]"

    def get_cells(self):
        return [cell.value for cell in self.cells.all().order_by("column__column_index")]


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

    class Meta:
        verbose_name = _("Task cell")
        verbose_name_plural = _("Task cells")

    @property
    def get_initial_value(self):
        return self._initial_value

    def __str__(self):
        return f"{self.business_process}[{self.column.column_index}, {self.task.index}] - {self.value}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_value = self.value


class TaskCellValueLog(mixins_models.TimestampModel):
    """Модель лога ячейки задачи"""

    id: int

    task_cell_id: int
    task_cell: TaskCell = models.ForeignKey(
        TaskCell, verbose_name=_("Task cell"), on_delete=models.CASCADE, related_name="logs"
    )

    old_value: str = models.TextField(verbose_name=_("Old value"))
    new_value: str = models.TextField(verbose_name=_("New value"))

    created_by_id: int
    created_by: User = models.ForeignKey(
        User, verbose_name=_("Created by"), on_delete=models.CASCADE, related_name="created_task_cell_values"
    )

    class Meta:
        verbose_name = _("Task cell value log")
        verbose_name_plural = _("Task cell value logs")

    def __str__(self):
        return f"{self.task_cell}[{self.old_value}, {self.new_value}]"
