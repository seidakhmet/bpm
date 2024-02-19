import re
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib.auth import models as django_auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _

from Crypto.PublicKey import RSA


from apps.common.mixins import models as mixin_models
from apps.users import BPMGroups
from apps.users.crypt import newkeys, decrypt, encrypt
from apps.users.managers import CustomUserManager, BPMGroupManager


class BPMGroup(mixin_models.TimestampModel):
    """Группы BPM"""

    id: int
    bpm_group_id: int = models.IntegerField(verbose_name=_("BPM group ID"), null=True, blank=True)
    bpm_group_name: str = models.CharField(verbose_name=_("BPM group name"), max_length=255, null=True, blank=True)

    objects = BPMGroupManager()

    class Meta:
        verbose_name = _("BPM Group")
        verbose_name_plural = _("BPM Groups")

    def __str__(self) -> str:
        return self.bpm_group_name

    @property
    def prefix(self):
        return BPMGroups.get_group(self.bpm_group_name)

    def code(self):
        return "".join(re.findall(r"\d+", self.bpm_group_name))


class User(mixin_models.TimestampModel, django_auth_models.AbstractUser):
    """Пользователи"""

    id: int

    is_developer: bool = models.BooleanField(verbose_name=_("Is developer"), default=False)

    bpm_user_id: int = models.IntegerField(verbose_name=_("BPM user ID"), null=True, blank=True)
    bpm_full_name: str = models.CharField(verbose_name=_("BPM full name"), max_length=255, null=True, blank=True)
    bpm_is_disabled: bool = models.BooleanField(verbose_name=_("BPM is disabled"), default=False)
    bpm_email: str = models.EmailField(verbose_name=_("BPM email"), null=True, blank=True)

    bpm_groups: models.ManyToManyField = models.ManyToManyField(
        BPMGroup, verbose_name=_("BPM groups"), blank=True, related_name="users"
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def full_name(self) -> str:
        return self.bpm_full_name or " ".join([self.first_name, self.last_name])

    def __str__(self) -> str:
        return self.full_name or self.username

    def bpm_group_prefixes(self):
        return [group.prefix for group in self.bpm_groups.all() if group.prefix]

    def bpm_group_codes(self):
        return [group.code() for group in self.bpm_groups.all() if group.code()]

    @property
    def can_edit(self):
        return any([group in BPMGroups.can_edit_tasks() for group in self.bpm_group_prefixes()])

    def bpm_group_share_prefixes(self):
        prefixes = [prefix for group in self.bpm_group_prefixes() for prefix in BPMGroups.can_share_with(group)]
        codes = self.bpm_group_codes()

        return [f"{prefix}_{code}" for prefix in prefixes for code in codes]


class RSAKey(mixin_models.TimestampModel, mixin_models.UUIDModel):
    """RSA ключи"""

    id: int
    name: str = models.CharField(verbose_name=_("Key name"), max_length=255, unique=True)
    public_key: str = models.TextField(blank=True, verbose_name=_("Public key"))
    private_key: str = models.TextField(blank=True, verbose_name=_("Private key"))

    is_active: bool = models.BooleanField(verbose_name=_("Is active"), default=True)
    is_test: bool = models.BooleanField(verbose_name=_("Is test"), default=False)

    class Meta:
        verbose_name = _("RSA Key")
        verbose_name_plural = _("RSA Keys")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.private_key or not self.public_key:
            public_key, private_key = newkeys(3072)
            self.public_key = public_key.exportKey().decode("utf-8")
            self.private_key = private_key.exportKey().decode("utf-8")
        super().save(*args, **kwargs)

    def get_private_key(self):
        return RSA.importKey(self.private_key)

    def get_public_key(self):
        return RSA.importKey(self.public_key)

    def encrypt(self, message: str):
        return encrypt(message, self.get_public_key()).decode()

    def decrypt(self, ciphertext: str):
        return decrypt(ciphertext, self.get_private_key()).decode()


class UserToken(mixin_models.TimestampModel, mixin_models.UUIDModel):
    """Токены пользователей"""

    id: int

    user_id: int
    user: User = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    is_used: bool = models.BooleanField(verbose_name=_("Is used"), default=False)
    rsa_key_uuid: str = models.CharField(verbose_name=_("RSA key UUID"), max_length=255)
    request_data: str = models.TextField(verbose_name=_("Request data"), null=True, blank=True)

    class Meta:
        verbose_name = _("User token")
        verbose_name_plural = _("User tokens")

    def __str__(self) -> str:
        return self.user.username

    @property
    def is_active(self) -> bool:
        if self.created_at:
            return (
                not (
                    self.created_at + timedelta(seconds=settings.AUTH_TOKEN_EXPIRE_SECONDS)
                    < datetime.now(tz=timezone(timedelta(hours=6)))
                )
                and not self.is_used
            )
