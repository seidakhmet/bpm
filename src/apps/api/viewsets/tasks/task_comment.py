from rest_framework import viewsets

from apps.tasks.models import TaskComment
from apps.api.serializers import TaskCommentSerializer


class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
