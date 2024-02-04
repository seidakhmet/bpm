from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from apps.api.serializers import TokenRequestSerializer
from apps.api.utils import decrypt_request
from apps.users.models import BPMGroup, UserToken


User = get_user_model()


class TokenRequestViewSet(mixins.CreateModelMixin, GenericViewSet):
    """Представление для получения токена"""

    serializer_class = TokenRequestSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uuid = serializer.validated_data["uuid"]
        encrypted_data = serializer.validated_data["data"]
        data, ok = decrypt_request(uuid, encrypted_data)
        if not ok:
            return Response({"data": None, "error": data["error"]}, status=status.HTTP_400_BAD_REQUEST)

        request_datetime = None
        try:
            request_datetime = datetime.strptime(data["date_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            return Response(
                {"data": None, "error": {"code": "Value error", "detail": "Неверный формат даты и времени"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request_datetime is None or datetime.utcnow() - request_datetime > timedelta(
            seconds=settings.BPM_POST_TOKEN_EXPIRE_SECONDS
        ):
            return Response(
                {"data": None, "error": {"code": "Value error", "detail": "Неверная дата и время"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if data.get("user_id", None) is None or data.get("user_name", None) is None:
            return Response(
                {"data": None, "error": {"code": "Value error", "detail": "Неверные данные"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if data.get("user_groups", None) is None or not isinstance(data["user_groups"], list):
            return Response(
                {"data": None, "error": {"code": "Value error", "detail": "Неверные данные"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        BPMGroup.objects.sync_groups_bpm()
        User.objects.sync_users_bpm(username=data["user_name"])

        user = User.objects.filter(bpm_user_id=data["user_id"], username=data["user_name"]).first()
        if user is None:
            return Response(
                {"data": None, "error": {"code": "Value error", "detail": "Пользователь не найден"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.is_active:
            return Response(
                {"data": None, "error": {"code": "Value error", "detail": "Пользователь не активен"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user.bpm_is_disabled:
            return Response(
                {"data": None, "error": {"code": "Value error", "detail": "Пользователь отключен в BPM"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_groups = [group.bpm_group_name for group in user.bpm_groups.all()]
        if not set(data["user_groups"]).issubset(set(user_groups)):
            return Response(
                {"data": None, "error": {"code": "Value error", "detail": "Пользователь не состоит в группе"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = UserToken.objects.create(user=user, request_data=encrypted_data, rsa_key_uuid=uuid)
        return Response({"data": {"token": token.uuid}, "error": None}, status=status.HTTP_200_OK)
