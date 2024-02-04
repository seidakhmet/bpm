from typing import Optional

from django.contrib.auth import models as django_auth_models
from django.db import models

from apps.users.services import BPMService

from django.apps import apps


class CustomUserManager(django_auth_models.UserManager):
    """Менеджер пользователей"""

    def sync_users_bpm(self, username: Optional[str] = None):
        """Синхронизация пользователей с BPM"""

        users, ok = BPMService().get_users(username=username)
        if ok:
            for user in users:
                groups = []
                if len(user["memberships"]) > 0:
                    for membership in user["memberships"]:
                        group = apps.get_model("users", "BPMGroup").objects.filter(bpm_group_name=membership).first()
                        if group:
                            groups.append(group)
                if len(groups) > 0:
                    instance, _ = self.model.objects.update_or_create(
                        bpm_user_id=user["userID"],
                        defaults={
                            "username": user["userName"],
                            "bpm_full_name": user["fullName"],
                            "bpm_is_disabled": user["isDisabled"],
                            "bpm_email": user["emailAddress"],
                        },
                    )
                    instance.bpm_groups.set(groups)


class BPMGroupManager(models.Manager):
    """Менеджер групп BPM"""

    def sync_groups_bpm(self):
        """Синхронизация групп с BPM"""

        groups, ok = BPMService().get_groups()
        if ok:
            for group in groups:
                self.model.objects.update_or_create(
                    bpm_group_id=group["groupID"],
                    defaults={
                        "bpm_group_name": group["groupName"],
                    },
                )
        else:
            return False
        return True
