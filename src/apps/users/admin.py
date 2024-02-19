from typing import Any

from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_object_actions import DjangoObjectActions, action

from apps.common.decorators.admin import require_confirmation
from apps.users.models import RSAKey, BPMGroup, UserToken


User = get_user_model()


class UserAdmin(DjangoObjectActions, auth_admin.UserAdmin):
    """Админка пользователей"""

    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": (
                    "username",
                    "password",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("BPM info"),
            {
                "fields": (
                    "bpm_user_id",
                    "bpm_full_name",
                    "bpm_is_disabled",
                    "bpm_email",
                    "bpm_groups",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_developer",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "changed_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "is_staff"),
            },
        ),
    )
    ordering = ("username",)
    readonly_fields = (
        "last_login",
        "created_at",
        "changed_at",
        "bpm_groups",
        "bpm_user_id",
        "bpm_full_name",
        "bpm_is_disabled",
        "bpm_email",
    )
    list_display = ("username", "full_name", "bpm_email", "user_groups")
    search_fields = (
        "username",
        "email",
        "bpm_groups__bpm_group_name",
        "bpm_full_name",
        "bpm_email",
        "first_name",
        "last_name",
        "bpm_user_id",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
    )

    @admin.display(description=_("Groups"))
    def user_groups(self, obj):
        """Получить группы, разделенные запятой, и отобразить пустую строку, если у пользователя нет групп."""
        user_groups = obj.bpm_groups.all()
        return "[{}]".format(", ".join([g.bpm_group_name for g in user_groups]))

    @admin.display(description=_("Full name"))
    def full_name(self, obj: User):
        """Получить полное имя пользователя."""
        return mark_safe(
            "<span{}>{}</span>{}".format(
                " style='font-weight: bold;'" if obj.is_staff else "",
                obj.full_name,
                ' <img src="/files/static/admin/img/icon-yes.svg" alt="False">' if obj.is_superuser else "",
            )
        )

    changelist_actions = [
        "sync_bpm_users",
    ]

    @require_confirmation(action=_("Sync BPM users"))
    @action(label=_("Sync BPM users"), description=_("Sync BPM users"))
    def sync_bpm_users(self, request: HttpRequest, queryset: QuerySet[Any]) -> None:
        """Синхронизировать группы BPM"""
        User.objects.sync_users_bpm()
        self.message_user(request, _("BPM users successfully synchronized."))


class RSAKeyAdmin(admin.ModelAdmin):
    """Админка RSA ключей"""

    fieldsets = (
        (
            _("RSA Key"),
            {
                "fields": (
                    "uuid",
                    "name",
                    "public_key",
                    "is_active",
                    "is_test",
                )
            },
        ),
    )
    readonly_fields = ("public_key", "private_key", "uuid")
    list_display = ("name", "uuid", "is_active", "is_test")
    list_filter = ("is_active", "is_test")
    search_fields = ("name", "uuid")


class BPMGroupAdmin(DjangoObjectActions, admin.ModelAdmin):
    """Админка групп BPM"""

    fieldsets = (
        (
            _("BPM Group"),
            {
                "fields": (
                    "bpm_group_id",
                    "bpm_group_name",
                )
            },
        ),
    )
    readonly_fields = ("bpm_group_id", "bpm_group_name")
    list_display = ("bpm_group_name", "bpm_group_id")
    search_fields = ("bpm_group_id", "bpm_group_name")

    changelist_actions = [
        "sync_bpm_groups",
    ]

    @require_confirmation(action=_("Sync BPM groups"))
    @action(label=_("Sync BPM groups"), description=_("Sync BPM groups"))
    def sync_bpm_groups(self, request: HttpRequest, queryset: QuerySet[Any]) -> None:
        """Синхронизировать группы BPM"""
        BPMGroup.objects.sync_groups_bpm()
        self.message_user(request, _("BPM groups successfully synchronized."))


class UserTokenAdmin(admin.ModelAdmin):
    """Админка токенов"""

    list_display = ("user", "uuid", "created_at", "is_used", "is_active")
    search_fields = ("user__username", "uuid")
    readonly_fields = ("uuid", "created_at", "rsa_key_uuid", "request_data", "is_active")  # "user",
    list_filter = ("is_used",)

    def is_active(self, obj):
        return mark_safe(
            '<img src="/files/static/admin/img/icon-yes.svg" alt="False">'
            if obj.is_active
            else '<img src="/files/static/admin/img/icon-no.svg" alt="False">'
        )

    is_active.short_description = _("Is active")


admin.site.register(User, UserAdmin)
admin.site.register(RSAKey, RSAKeyAdmin)
admin.site.register(BPMGroup, BPMGroupAdmin)
admin.site.register(UserToken, UserTokenAdmin)
