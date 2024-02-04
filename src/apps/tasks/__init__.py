from django.db import models
from django.utils.translation import gettext_lazy as _


class BusinessProcessStatuses(models.TextChoices):
    """Статусы бизнес-процесса"""

    CREATED = "created", _("Created")
    PREPARED_FOR_PUBLISHING = "prepared_for_publishing", _("Prepared for publishing")
    PUBLISHED = "published", _("Published")
    IN_PROGRESS = "in_progress", _("In progress")
    COMPLETED = "completed", _("Completed")
    CANCELED = "canceled", _("Canceled")


class TaskColumnTypes(models.TextChoices):
    """Типы колонок задачи"""

    STRING = "string", _("String")
    TEXT = "text", _("Text")
    INTEGER = "integer", _("Integer")
    FLOAT = "float", _("Float")
    DATE = "date", _("Date")
    DATE_TIME = "date_time", _("Date and time")
    BOOLEAN = "boolean", _("Boolean")


class TaskDelegationStatuses(models.TextChoices):
    """Статусы делегирования задачи"""

    CREATED = "created", _("Created")
    RECEIVED = "received", _("Received")
    FINISHED = "finished", _("Finished")
    ACCEPTED = "accepted", _("Accepted")
    REJECTED = "rejected", _("Rejected")
    CANCELED = "canceled", _("Canceled")


class ExcelFileParserType(models.TextChoices):
    """Типы парсера Excel файла"""

    DGD_CODE_AND_DGD_TITLE = "dgd_code_and_dgd_title", _("DGD code and DGD title")
    DGD_CODE_AND_DGD_TITLE_AND_UGD_CODE = "dgd_code_and_dgd_title_and_ugd_code", _(
        "DGD code and DGD title and UGD code"
    )


class ExcelColumnIndex(models.IntegerChoices):
    """Индексы колонок Excel файла"""

    A = 0, _("A column")
    B = 1, _("B column")
    C = 2, _("C column")
    D = 3, _("D column")
    E = 4, _("E column")
    F = 5, _("F column")
    G = 6, _("G column")
    H = 7, _("H column")
    I = 8, _("I column")
    J = 9, _("J column")
    K = 10, _("K column")
    L = 11, _("L column")
    M = 12, _("M column")
    N = 13, _("N column")
    O = 14, _("O column")
    P = 15, _("P column")
    Q = 16, _("Q column")
    R = 17, _("R column")
    S = 18, _("S column")
    T = 19, _("T column")
    U = 20, _("U column")
    V = 21, _("V column")
    W = 22, _("W column")
    X = 23, _("X column")
    Y = 24, _("Y column")
    Z = 25, _("Z column")
