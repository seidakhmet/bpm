import json
from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase

from apps.api.utils import decrypt_request
from apps.users.models import RSAKey


class APITests(APITestCase):
    """Тестирование API"""

    rsa_key = None

    def setUp(self):
        """Настройка тестирования"""
        self.rsa_key = RSAKey.objects.create(name="test", is_active=True, is_test=True)

    def test_post_token(self):
        """Тестирование получения токена"""
        data_for_encrypt = {
            "user_id": 1807,
            "user_name": "nzh_muratbekov",
            "date_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "user_groups": ["BPM_KGD"],
        }
        encrypted_data = self.rsa_key.encrypt(json.dumps(data_for_encrypt))

        response = self.client.post(
            "/api/v1/token/",
            {
                "uuid": self.rsa_key.uuid,
                "data": encrypted_data,
            },
            format="json",
        )
        data = response.json()

        print(data)
        self.assertEqual(status.HTTP_200_OK, response.status_code, msg="Статус ответа не 200")
        self.assertEqual(True, isinstance(data, dict), msg="Ответ не является словарем")
        self.assertEqual(True, isinstance(data.get("data", None), dict), msg="Ответ не содержит словарь data")
        self.assertEqual(True, isinstance(data.get("data", {}).get("token", None), str), msg="Ответ не содержит токен")
        self.assertEqual(True, isinstance(data.get("error", None), dict), msg="Ответ не содержит словарь error")
        self.assertEqual(None, data.get("error", None), msg="Ошибка при получении токена")
        token = data.get("data", {}).get("token", None)
        self.assertEqual(True, isinstance(token, str), msg="Токен не является строкой")
        self.assertEqual(True, len(token) > 0, msg="Токен не содержит символов")
