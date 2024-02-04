from rest_framework import serializers

from apps.tasks.models import BusinessProcess


class BusinessProcessSerializer(serializers.ModelSerializer):
    creator_full_name = serializers.CharField(source="created_by.full_name", read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = BusinessProcess
        fields = (
            "id",
            "title",
            "description",
            "excel_file",
            "status",
            "deadline",
            "min_bpm_group",
            "creator_full_name",
        )
        read_only_fields = ["id"]
