import base64
import logging
import requests
from typing import Optional

from django.conf import settings

logger = logging.getLogger(__name__)


class BPMService:
    """Сервис для работы с BPM"""

    username = settings.BPM_USERNAME
    password = settings.BPM_PASSWORD

    def get_auth_token(self):
        return "Basic {}".format(base64.b64encode(f"{self.username}:{self.password}".encode("utf-8")).decode("utf-8"))

    def get_users(self, username: Optional[str] = None) -> tuple[list[dict], bool]:
        url = (
            f"https://{settings.BPM_HOST}/bpm/rest/bpm/wle/v1/users?includeTaskExperts=true"
            f"&sort=true&includeInternalMemberships=false&refreshUser=false&parts=memberships"
        )
        if username:
            url += f"&filter={username}"
        response_data = []
        try:
            requests.packages.urllib3.disable_warnings()
            response = requests.get(
                url,
                headers={
                    "Authorization": self.get_auth_token(),
                    "Accept": "application/json",
                },
                verify=False,
            )
            response.raise_for_status()
            return response.json()["data"]["users"], True
        except Exception as e:
            logger.error(f"Ошибка при получении пользователей из BPM: {e}")
            return response_data, False

    def get_groups(self) -> tuple[list[dict], bool]:
        url = f"https://{settings.BPM_HOST}/bpm/rest/bpm/wle/v1/groups?filter=BPM_*&includeDeleted=false&parts=none"
        response_data = []
        try:
            requests.packages.urllib3.disable_warnings()
            response = requests.get(
                url,
                headers={
                    "Authorization": self.get_auth_token(),
                    "Accept": "application/json",
                },
                verify=False,
            )
            response.raise_for_status()
            return response.json()["data"]["groups"], True
        except Exception as e:
            logger.error(f"Ошибка при получении групп из BPM: {e}")
            return response_data, False
