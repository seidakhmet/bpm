from rest_framework import viewsets

from apps.tasks.models import BusinessProcess
from apps.api.serializers import BusinessProcessSerializer


class BusinessProcessViewSet(viewsets.ModelViewSet):
    queryset = BusinessProcess.objects.all()
    serializer_class = BusinessProcessSerializer
