from django.utils.translation import gettext as _


class ParserFactory:
    """Фабрика парсеров"""

    @staticmethod
    def get_parser(business_process: "BusinessProcess"):
        """Создание парсера"""
        if business_process.excel_file:
            from .excel_parser import ExcelParser

            return ExcelParser(business_process)
        raise ValueError(_("Excel file is not found"))
