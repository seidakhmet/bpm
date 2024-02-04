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

    def can_share_with(self) -> list:
        if self == self.KGD:
            return [self.DGD_RUK_ZAM]
        elif self == self.DGD_RUK_ZAM:
            return [self.DGD_RUK_UPR, self.DGD_NACH_OTD, self.DGD_ISP]
        elif self == self.DGD_RUK_UPR:
            return [self.DGD_NACH_OTD, self.DGD_ISP]
        elif self == self.DGD_NACH_OTD:
            return [self.DGD_ISP]
        elif self == self.DGD_ISP:
            return [self.UGD_RUK_ZAM]
        elif self == self.UGD_RUK_ZAM:
            return [self.UGD_RUK_OTD, self.UGD_ISP]
        elif self == self.UGD_RUK_OTD:
            return [self.UGD_ISP]
        return []
