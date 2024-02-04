from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.tasks.models import BusinessProcess


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        business_processes = BusinessProcess.objects.filter(created_by=request.user).order_by("-created_at")
        return render(request, "web/pages/index.html", {"business_processes": business_processes})
