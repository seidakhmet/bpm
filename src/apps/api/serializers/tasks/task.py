from rest_framework import serializers

from apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "business_process",
            "index",
            "dgd_code",
            "dgd_name",
            "ugd_code",
            "status",
            "created_at_pretty",
        )
        read_only_fields = [
            "id",
            "business_process",
            "index",
            "dgd_code",
            "dgd_name",
            "ugd_code",
            "status",
            "created_at_pretty",
        ]
