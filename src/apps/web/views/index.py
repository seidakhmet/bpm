from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views import View

from apps.tasks.models import BusinessProcess


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        business_processes = (
            BusinessProcess.objects.filter(
                Q(
                    Q(created_by=request.user)
                    | Q(tasks__delegations__delegated_to=request.user)
                    | Q(tasks__delegations__delegated_to_bpm_group__users=request.user)
                )
            )
            .order_by("-created_at")
            .distinct()
        )
        return render(request, "web/pages/index.html", {"business_processes": business_processes})
