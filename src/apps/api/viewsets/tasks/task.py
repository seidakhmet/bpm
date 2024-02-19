from rest_framework import viewsets, response
from rest_framework.decorators import action

from apps.tasks.models import Task
from apps.api.serializers import TaskSerializer, TaskCommentSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        task = self.get_object()
        comments = task.comments.all()
        serializer = TaskCommentSerializer(comments, many=True)
        return response.Response(serializer.data)
