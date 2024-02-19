import pandas as pd
import numpy as np
import re

from django.db import transaction

from apps.tasks.models import BusinessProcess
from apps.tasks import TaskColumnTypes


@transaction.atomic
class ExcelParser:
    """Парсер для файлов excel"""

    def __init__(self, business_process: BusinessProcess):
        self.business_process = business_process

    def parse(self):
        """Парсинг файла excel"""
        workbook = pd.read_excel(self.business_process.excel_file)
        workbook = workbook.replace(np.nan, None, regex=True)

        column_index = 0
        for column in workbook.columns:
            self.business_process.columns.update_or_create(
                column_index=column_index,
                defaults={
                    "column_name": column,
                    "column_type": TaskColumnTypes.STRING,
                },
            )
            column_index += 1

        index = 0
        for row in workbook.values:
            task, _ = self.business_process.tasks.update_or_create(
                index=index,
                defaults={
                    "dgd_code": row[self.business_process.dgd_code_column],
                    "dgd_code_number": "".join(re.findall(r"\d+", row[self.business_process.dgd_code_column])),
                    "dgd_name": row[self.business_process.dgd_name_column],
                },
            )
            index += 1
            if task:
                for task_column in self.business_process.columns.all().order_by("column_index"):
                    self.business_process.cells.update_or_create(
                        task=task,
                        column=task_column,
                        defaults={"value": row[task_column.column_index]},
                    )
