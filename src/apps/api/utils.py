import json
import uuid as _uuid

from django.utils.translation import gettext_lazy as _

from apps.users.models import RSAKey


def decrypt_request(uuid: _uuid.UUID, data: str) -> tuple[dict, bool]:
    """Расшифровка запроса"""
    rsa_key = RSAKey.objects.filter(uuid=uuid).first()
    if not rsa_key:
        return {"error": _("RSA key not found")}, False
    try:
        message = rsa_key.decrypt(data)
    except Exception as e:
        return {"error": str(e)}, False

    return (
        json.loads(
            message,
        ),
        True,
    )
