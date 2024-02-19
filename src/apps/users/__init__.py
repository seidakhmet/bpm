from django.db.models import TextChoices


class BPMGroups(TextChoices):
    KGD = "BPM_KGD", "БПМ КГД"
    DGD_RUK_ZAM = "BPM_DGD_RUK_ZAM", "БПМ ДГД Руководитель заместитель"
    DGD_RUK_UPR = "BPM_DGD_RUK_UPR", "БПМ ДГД Руководитель управления"
    DGD_NACH_OTD = "BPM_DGD_NACH_OTD", "БПМ ДГД Начальник отдела"
    DGD_ISP = "BPM_DGD_ISP", "БПМ ДГД Исполнитель"

    UGD_RUK_ZAM = "BPM_UGD_RUK_ZAM", "БПМ УГД Руководитель заместитель"
    UGD_RUK_OTD = "BPM_UGD_RUK_OTD", "БПМ УГД Руководитель отдела"
    UGD_ISP = "BPM_UGD_ISP", "БПМ УГД Исполнитель"

    @classmethod
    def can_share_with(cls, value) -> list:
        if value == cls.KGD:
            return [cls.DGD_RUK_ZAM]
        elif value == cls.DGD_RUK_ZAM:
            return [cls.DGD_RUK_UPR, cls.DGD_NACH_OTD, cls.DGD_ISP]
        elif value == cls.DGD_RUK_UPR:
            return [cls.DGD_NACH_OTD, cls.DGD_ISP, cls.UGD_RUK_ZAM]  # TODO: Убрать UGD_RUK_ZAM
        elif value == cls.DGD_NACH_OTD:
            return [cls.DGD_ISP]
        elif value == cls.DGD_ISP:
            return [cls.UGD_RUK_ZAM]
        elif value == cls.UGD_RUK_ZAM:
            return [cls.UGD_RUK_OTD, cls.UGD_ISP]
        elif value == cls.UGD_RUK_OTD:
            return [cls.UGD_ISP]
        return []

    @classmethod
    def can_edit_tasks(cls) -> list:
        return [cls.DGD_ISP, cls.UGD_ISP, cls.DGD_NACH_OTD]

    @classmethod
    def get_group(cls, name: str):
        for group in cls:
            if name.startswith(group.value):
                return group
        return None
