from rest_framework import serializers

from apps.tasks.models import TaskComment


class TaskCommentSerializer(serializers.ModelSerializer):
    creator_full_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = TaskComment
        fields = (
            "id",
            "task",
            "text",
            "creator_full_name",
            "created_at_pretty",
        )
        read_only_fields = ["id", "created_at_pretty", "creator_full_name"]
