from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.edit import DeleteView

from apps.web.forms import BusinessProcessForm


class AddBusinessProcessView(LoginRequiredMixin, generic.CreateView):
    form_class = BusinessProcessForm
    template_name = "web/pages/add.business-process.html"

    def get_success_url(self):
        return reverse_lazy("detail-business-process", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DetailBusinessProcessView(LoginRequiredMixin, generic.DetailView):
    template_name = "web/pages/detail.business-process.html"

    def get_queryset(self):
        return self.request.user.created_business_processes.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["columns"] = self.object.columns.all().order_by("column_index")
        return self.render_to_response(context)


class EditBusinessProcessView(LoginRequiredMixin, generic.UpdateView):
    form_class = BusinessProcessForm
    template_name = "web/pages/edit.business-process.html"

    def get_success_url(self):
        return reverse_lazy("detail-business-process", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        return self.request.user.created_business_processes.all()


class DeleteBusinessProcessView(LoginRequiredMixin, DeleteView):
    template_name = "web/pages/delete.business-process.html"
    success_url = reverse_lazy("index")

    def get_queryset(self):
        return self.request.user.created_business_processes.all()


class EditBusinessProcessColumnView(LoginRequiredMixin, generic.DetailView):
    template_name = "web/pages/edit-columns.business-process.html"

    def get_queryset(self):
        return self.request.user.created_business_processes.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["columns"] = self.object.columns.all().order_by("column_index")
        return self.render_to_response(context)
