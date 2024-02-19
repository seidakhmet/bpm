from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q, Case, When, BooleanField, Max, IntegerField, OuterRef, Subquery
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.views.generic.edit import DeleteView

from apps.web.forms import BusinessProcessForm, TaskStatusForm, PublishBusinessProcessForm
from apps.tasks import TaskColumnTypes, models as tasks_models, TaskDelegationStatuses, BusinessProcessStatuses
from apps.users import BPMGroups, models as users_models


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
        return tasks_models.BusinessProcess.objects.filter(
            Q(
                Q(created_by=self.request.user)
                | Q(tasks__delegations__delegated_to=self.request.user)
                | Q(tasks__delegations__delegated_to_bpm_group__users=self.request.user)
            )
        ).distinct()

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


class PublishBusinessProcessView(LoginRequiredMixin, generic.UpdateView):
    form_class = PublishBusinessProcessForm
    template_name = "web/pages/publish.business-process.html"

    def get_success_url(self):
        return reverse_lazy("detail-business-process", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        return self.request.user.created_business_processes.all()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "publish" in request.POST:
            self.object.status = BusinessProcessStatuses.PUBLISHED
            self.object.save(run_parser=False)
            for task in self.object.tasks.all():
                delegate_to = users_models.BPMGroup.objects.filter(
                    bpm_group_name=f"BPM_DGD_RUK_ZAM_{task.dgd_code_number}"
                ).first()
                if delegate_to:
                    tasks_models.TaskDelegation.objects.create(
                        task=task,
                        delegated_to_bpm_group=delegate_to,
                        created_by=self.object.created_by,
                        status=TaskDelegationStatuses.DELEGATED_TO_GROUP,
                    )
            return HttpResponseRedirect(self.get_success_url())
        return super().post(request, *args, **kwargs)


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
        context["column_types"] = TaskColumnTypes
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = request.POST
        for column in self.object.columns.all():
            column_name = data.get(f"column_name_{column.pk}")
            column_type = data.get(f"column_type_{column.pk}")
            is_editable = data.get(f"is_editable_{column.pk}", False) == "on"
            column.column_name = column_name
            column.column_type = column_type
            column.is_editable = is_editable
            column.save()
        return HttpResponseRedirect(reverse("detail-business-process", kwargs={"pk": self.object.pk}))


class StatusDetailBusinessProcessView(LoginRequiredMixin, generic.DetailView):
    template_name = "web/pages/statuses.detail.business-process.html"

    def get_queryset(self):
        return self.request.user.created_business_processes.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["statuses"] = self.object.statuses.all().order_by("created_at")
        return self.render_to_response(context)


class AddTaskStatusView(LoginRequiredMixin, generic.CreateView):
    form_class = TaskStatusForm
    template_name = "web/pages/form.status.business-process.html"

    def get_success_url(self):
        return reverse_lazy("status-detail-business-process", kwargs={"pk": self.object.business_process.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["form"].fields["required_task_columns"].queryset = self.object.columns.filter(is_editable=True)
        return self.render_to_response(context)

    def get_queryset(self):
        return self.request.user.created_business_processes.all()

    def form_valid(self, form):
        form.instance.business_process = self.get_object()
        return super().form_valid(form)


class EditTaskStatusView(LoginRequiredMixin, generic.UpdateView):
    form_class = TaskStatusForm
    template_name = "web/pages/form.status.business-process.html"

    def get_success_url(self):
        return reverse_lazy("status-detail-business-process", kwargs={"pk": self.object.business_process.pk})

    def get_queryset(self):
        return tasks_models.TaskStatus.objects.filter(business_process__created_by=self.request.user)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["form"].fields["required_task_columns"].queryset = self.object.business_process.columns.filter(
            is_editable=True
        )
        return self.render_to_response(context)


class DeleteTaskStatusView(LoginRequiredMixin, DeleteView):
    template_name = "web/pages/status.delete.business-process.html"

    def get_success_url(self):
        return reverse_lazy("status-detail-business-process", kwargs={"pk": self.object.business_process.pk})

    def get_queryset(self):
        return tasks_models.TaskStatus.objects.filter(business_process__created_by=self.request.user)


class TaskView(LoginRequiredMixin, generic.DetailView):
    template_name = "web/pages/tasks.business-process.html"
    last_delegation_status_subquery = (
        tasks_models.TaskDelegation.objects.filter(task=OuterRef("pk")).order_by("-created_at").values("status")[:1]
    )
    last_delegation_delegated_to_subquery = (
        tasks_models.TaskDelegation.objects.filter(task=OuterRef("pk"))
        .order_by("-created_at")
        .values("delegated_to")[:1]
    )
    last_delegation_delegated_to_bpm_group_subquery = (
        tasks_models.TaskDelegation.objects.filter(task=OuterRef("pk"))
        .order_by("-created_at")
        .values("delegated_to_bpm_group")[:1]
    )
    last_delegation_created_by_subquery = (
        tasks_models.TaskDelegation.objects.filter(task=OuterRef("pk")).order_by("-created_at").values("created_by")[:1]
    )

    def get_queryset(self):
        queryset = tasks_models.BusinessProcess.objects.filter(
            Q(created_by=self.request.user)
            | Q(tasks__delegations__delegated_to=self.request.user)
            | Q(tasks__delegations__delegated_to_bpm_group__in=self.request.user.bpm_groups.all())
        ).distinct()
        return queryset

    def my_tasks(self, request, query: str = ""):
        queryset = (
            self.object.tasks.prefetch_related("cells", "delegations")
            .annotate(
                last_delegation_status=Subquery(self.last_delegation_status_subquery),
                last_delegation_delegated_to=Subquery(self.last_delegation_delegated_to_subquery),
                last_delegation_delegated_to_bpm_group=Subquery(self.last_delegation_delegated_to_bpm_group_subquery),
                last_delegation_created_by=Subquery(self.last_delegation_created_by_subquery),
            )
            .filter(
                last_delegation_delegated_to=request.user,
                last_delegation_status__in=[
                    TaskDelegationStatuses.DELEGATED_TO_USER,
                    TaskDelegationStatuses.SELF_DELEGATED,
                    TaskDelegationStatuses.RETURNED_TO_DELEGATOR,
                    TaskDelegationStatuses.SENT_TO_REWORK,
                ],
            )
            .exclude(
                last_delegation_status__in=[
                    TaskDelegationStatuses.DELEGATED_TO_GROUP,
                    TaskDelegationStatuses.SENT_TO_APPROVAL,
                ],
            )
            .annotate(comments_count=Count("comments"))
            .order_by("index")
            .distinct()
        )
        if query:
            queryset = queryset.filter(cells__value__icontains=query).distinct()
        return queryset

    def group_tasks(self, request, query: str = ""):
        queryset = (
            self.object.tasks.prefetch_related("cells", "delegations")
            .annotate(
                last_delegation_status=Subquery(self.last_delegation_status_subquery),
                last_delegation_delegated_to=Subquery(self.last_delegation_delegated_to_subquery),
                last_delegation_delegated_to_bpm_group=Subquery(self.last_delegation_delegated_to_bpm_group_subquery),
                last_delegation_created_by=Subquery(self.last_delegation_created_by_subquery),
            )
            .filter(
                last_delegation_delegated_to_bpm_group__in=request.user.bpm_groups.all(),
                last_delegation_status__in=[
                    TaskDelegationStatuses.DELEGATED_TO_GROUP,
                ],
            )
            .exclude(
                last_delegation_status__in=[
                    TaskDelegationStatuses.DELEGATED_TO_USER,
                    TaskDelegationStatuses.SELF_DELEGATED,
                    TaskDelegationStatuses.RETURNED_TO_DELEGATOR,
                    TaskDelegationStatuses.SENT_TO_APPROVAL,
                    TaskDelegationStatuses.SENT_TO_REWORK,
                ]
            )
            .annotate(
                comments_count=Count("comments"),
            )
            .order_by("index")
            .distinct()
        )

        if query:
            queryset = queryset.filter(cells__value__icontains=query).distinct()
        return queryset

    def delegated_tasks(self, request, query: str = ""):
        queryset = (
            self.object.tasks.prefetch_related("cells", "delegations")
            .annotate(
                last_delegation_status=Subquery(self.last_delegation_status_subquery),
                last_delegation_delegated_to=Subquery(self.last_delegation_delegated_to_subquery),
                last_delegation_delegated_to_bpm_group=Subquery(self.last_delegation_delegated_to_bpm_group_subquery),
                last_delegation_created_by=Subquery(self.last_delegation_created_by_subquery),
            )
            .filter(
                delegations__created_by=request.user,
                delegations__status__in=[
                    TaskDelegationStatuses.DELEGATED_TO_USER,
                    TaskDelegationStatuses.DELEGATED_TO_GROUP,
                    TaskDelegationStatuses.SENT_TO_REWORK,
                ],
            )
            .exclude(
                last_delegation_created_by=request.user,
                last_delegation_status__in=[
                    TaskDelegationStatuses.SENT_TO_APPROVAL,
                ],
            )
            .exclude(
                last_delegation_delegated_to=request.user,
                last_delegation_status__in=[
                    TaskDelegationStatuses.SENT_TO_APPROVAL,
                    TaskDelegationStatuses.SENT_TO_REWORK,
                ],
            )
            .order_by("index")
            .distinct()
        )
        print(queryset.query)
        if query:
            queryset = queryset.filter(cells__value__icontains=query).distinct()
        return queryset

    def approve_tasks(self, request, query: str = ""):
        queryset = (
            self.object.tasks.prefetch_related("cells", "delegations")
            .annotate(
                last_delegation_status=Subquery(self.last_delegation_status_subquery),
                last_delegation_delegated_to=Subquery(self.last_delegation_delegated_to_subquery),
                last_delegation_delegated_to_bpm_group=Subquery(self.last_delegation_delegated_to_bpm_group_subquery),
                last_delegation_created_by=Subquery(self.last_delegation_created_by_subquery),
            )
            .filter(
                last_delegation_delegated_to=request.user,
                last_delegation_status__in=[
                    TaskDelegationStatuses.SENT_TO_APPROVAL,
                ],
            )
            .exclude(
                last_delegation_status__in=[
                    TaskDelegationStatuses.DELEGATED_TO_USER,
                    TaskDelegationStatuses.DELEGATED_TO_GROUP,
                    TaskDelegationStatuses.SELF_DELEGATED,
                    TaskDelegationStatuses.RETURNED_TO_DELEGATOR,
                    TaskDelegationStatuses.SENT_TO_REWORK,
                ],
            )
            .order_by("index")
            .distinct()
        )
        if query:
            queryset = queryset.filter(cells__value__icontains=query).distinct()
        return queryset

    def get_tasks_queryset(self, request, query: str = ""):
        return self.my_tasks(request, query)

    def get_tasks(self, request):
        query = request.GET.get("query", "")
        page_number = request.GET.get("page", 1)
        queryset = self.get_tasks_queryset(request, query)
        paginator = Paginator(queryset, 50)
        page_obj = paginator.get_page(page_number)
        context = self.get_context_data(object=self.object)

        context["columns"] = self.object.columns.all().order_by("column_index")
        context["columns_count"] = len(context["columns"]) + 5
        context["my_tasks_count"] = self.my_tasks(request).count()
        context["group_tasks_count"] = self.group_tasks(request).count()
        context["delegated_tasks_count"] = self.delegated_tasks(request).count()
        context["approve_tasks_count"] = self.approve_tasks(request).count()

        context["query"] = query

        context["tasks"] = page_obj
        context["statuses"] = self.object.statuses.all().order_by("status_name")
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_tasks(request)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = request.POST
        is_save = data.get("save", False)
        is_delegating = data.get("delegating", False)
        is_delegate = data.get("delegate", False)
        send_to_approve = data.get("send_to_approve", False)
        send_to_approve_confirm = data.get("send_to_approve_confirm", False)
        context = self.get_tasks(request)
        if is_save:
            cells = [{k: v} for k, v in data.items() if k.startswith("cell_") and v != ""]
            for cell in cells:
                cell_pk = list(cell.keys())[0].split("_")[1]
                cell_value = cell[list(cell.keys())[0]]
                cell_instance = tasks_models.TaskCell.objects.get(pk=cell_pk)
                cell_instance.value = cell_value
                cell_instance.save()
                if cell_instance.get_initial_value != cell_instance.value:
                    tasks_models.TaskCellValueLog.objects.create(
                        created_by=request.user,
                        task_cell=cell_instance,
                        old_value=cell_instance.get_initial_value,
                        new_value=cell_instance.value,
                    )
            statuses = [{k: v} for k, v in data.items() if k.startswith("row_status_") and v != "0"]
            for status in statuses:
                task_pk = list(status.keys())[0].split("_")[2]
                task_instance = tasks_models.Task.objects.get(pk=task_pk)
                task_instance.status = tasks_models.TaskStatus.objects.get(pk=status[list(status.keys())[0]])
                task_instance.save()

        elif is_delegating:
            selected_rows = [v for k, v in data.items() if k.startswith("selected_row_") and v != ""]
            context["delegated_tasks_count"] = len(selected_rows)
            context["tasks"] = tasks_models.Task.objects.filter(pk__in=selected_rows)

            context["bpm_groups"] = []
            for group in self.request.user.bpm_group_prefixes():
                context["bpm_groups"] += BPMGroups.can_share_with(group)

            prefixes = self.request.user.bpm_group_share_prefixes()
            q_objects = Q()
            for prefix in prefixes:
                q_objects |= Q(bpm_group_name__startswith=prefix)
            bpm_groups = users_models.BPMGroup.objects.filter(q_objects)
            context["bpm_users"] = [
                user for group in bpm_groups for user in group.users.all() if user != self.request.user
            ]

            return self.response_class(
                request=self.request,
                template="web/pages/delegating.business-process.html",
                context=context,
                using=self.template_engine,
            )
        elif is_delegate:
            selected_rows = [v for k, v in data.items() if k.startswith("row_id_") and v != ""]
            delegated_to = data.get("user_or_group", False)
            if delegated_to and selected_rows:
                if delegated_to.startswith("group__"):
                    for row in selected_rows:
                        task = tasks_models.Task.objects.get(pk=row)
                        delegate_to = users_models.BPMGroup.objects.get(
                            bpm_group_name=f"{delegated_to.split('__')[1]}_{task.ugd_code if task.ugd_code else task.dgd_code_number}"
                        )
                        tasks_models.TaskDelegation.objects.create(
                            task=task,
                            delegated_to_bpm_group=delegate_to,
                            created_by=request.user,
                            status=TaskDelegationStatuses.DELEGATED_TO_GROUP,
                        )
                if delegated_to.startswith("user__"):
                    delegate_to = users_models.User.objects.get(pk=delegated_to.split("__")[1])
                    for row in selected_rows:
                        task = tasks_models.Task.objects.get(pk=row)
                        tasks_models.TaskDelegation.objects.create(
                            task=task,
                            delegated_to=delegate_to,
                            created_by=request.user,
                            status=TaskDelegationStatuses.DELEGATED_TO_USER,
                        )
        elif send_to_approve:
            selected_rows = [v for k, v in data.items() if k.startswith("selected_row_") and v != ""]
            context["send_to_approve_tasks_count"] = len(selected_rows)
            context["tasks"] = tasks_models.Task.objects.filter(pk__in=selected_rows)
            return self.response_class(
                request=self.request,
                template="web/pages/send-to-approve-confirm.business-process.html",
                context=context,
                using=self.template_engine,
            )
        elif send_to_approve_confirm:
            selected_rows = [v for k, v in data.items() if k.startswith("row_id_") and v != ""]
            tasks = tasks_models.Task.objects.filter(pk__in=selected_rows).prefetch_related("delegations")
            for task in tasks:
                last_delegation = task.get_user_last_delegation(request.user)
                tasks_models.TaskDelegation.objects.create(
                    task=task,
                    delegated_to=last_delegation.created_by,
                    created_by=request.user,
                    status=TaskDelegationStatuses.SENT_TO_APPROVAL,
                )

        return redirect(
            reverse("tasks-business-process", kwargs={"pk": self.object.pk}) + "?" + request.GET.urlencode()
        )


class GroupTaskView(TaskView):
    template_name = "web/pages/group-tasks.business-process.html"

    def get_tasks_queryset(self, request, query: str = ""):
        return self.group_tasks(request, query)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_tasks(request)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = request.POST
        assign_all_to_me = data.get("assign_all_to_me", False)
        assign = data.get("assign", False)
        assign_all = data.get("assign_all", False)
        assign_confirm = data.get("assign_confirm", False)
        context = self.get_tasks(request)
        if assign_all_to_me:
            return self.response_class(
                request=self.request,
                template="web/pages/assign-all.business-process.html",
                context=context,
                using=self.template_engine,
            )
        elif assign:
            selected_rows = [v for k, v in data.items() if k.startswith("selected_row_") and v != ""]
            context["assign_tasks_count"] = len(selected_rows)
            context["tasks"] = tasks_models.Task.objects.filter(pk__in=selected_rows)
            return self.response_class(
                request=self.request,
                template="web/pages/assign-confirm.business-process.html",
                context=context,
                using=self.template_engine,
            )
        elif assign_all:
            tasks = self.group_tasks(request)
            for task in tasks:
                last_delegation = task.get_last_delegation_instance()
                if not last_delegation or last_delegation and last_delegation.delegated_to is None:
                    tasks_models.TaskDelegation.objects.create(
                        task=task,
                        delegated_to=request.user,
                        created_by=request.user,
                        status=TaskDelegationStatuses.SELF_DELEGATED,
                    )
        elif assign_confirm:
            selected_rows = [v for k, v in data.items() if k.startswith("row_id_") and v != ""]
            tasks = tasks_models.Task.objects.filter(pk__in=selected_rows).prefetch_related("delegations")
            for task in tasks:
                last_delegation = task.get_last_delegation_instance()
                if not last_delegation or last_delegation and last_delegation.delegated_to is None:
                    tasks_models.TaskDelegation.objects.create(
                        task=task,
                        delegated_to=request.user,
                        created_by=request.user,
                        status=TaskDelegationStatuses.SELF_DELEGATED,
                    )

        return redirect(
            reverse("group-tasks-business-process", kwargs={"pk": self.object.pk}) + "?" + request.GET.urlencode()
        )


class DelegatedTaskView(TaskView):
    template_name = "web/pages/delegated-tasks.business-process.html"

    def get_tasks_queryset(self, request, query: str = ""):
        return self.delegated_tasks(request, query)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_tasks(request)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pass


class ApproveTaskView(TaskView):
    template_name = "web/pages/approve-tasks.business-process.html"

    def get_tasks_queryset(self, request, query: str = ""):
        return self.approve_tasks(request, query)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_tasks(request)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = request.POST
        approve = data.get("approve", False)
        reject = data.get("reject", False)
        context = self.get_tasks(request)
        if approve:
            selected_rows = [v for k, v in data.items() if k.startswith("selected_row_") and v != ""]
            context["delegated_tasks_count"] = len(selected_rows)
            context["tasks"] = tasks_models.Task.objects.filter(pk__in=selected_rows)
            return self.response_class(
                request=self.request,
                template="web/pages/approve-confirm.business-process.html",
                context=context,
                using=self.template_engine,
            )
        elif data.get("approved", False):
            selected_rows = [v for k, v in data.items() if k.startswith("row_id_") and v != ""]
            tasks = tasks_models.Task.objects.filter(pk__in=selected_rows).prefetch_related("delegations")
            for task in tasks:
                last_delegation = task.get_user_last_delegation(request.user)
                tasks_models.TaskDelegation.objects.create(
                    task=task,
                    delegated_to=last_delegation.created_by,
                    created_by=request.user,
                    status=TaskDelegationStatuses.SENT_TO_APPROVAL,
                )
        elif reject:
            selected_rows = [v for k, v in data.items() if k.startswith("selected_row_") and v != ""]
            context["approve_tasks_count"] = len(selected_rows)
            context["tasks"] = tasks_models.Task.objects.filter(pk__in=selected_rows)
            return self.response_class(
                request=self.request,
                template="web/pages/reject-confirm.business-process.html",
                context=context,
                using=self.template_engine,
            )
        elif data.get("rejected", False):
            selected_rows = [v for k, v in data.items() if k.startswith("row_id_") and v != ""]
            tasks = tasks_models.Task.objects.filter(pk__in=selected_rows).prefetch_related("delegations")
            for task in tasks:
                last_delegation = task.get_last_approve_delegation()
                tasks_models.TaskDelegation.objects.create(
                    task=task,
                    delegated_to=last_delegation.created_by,
                    created_by=request.user,
                    status=TaskDelegationStatuses.SENT_TO_REWORK,
                )
        return redirect(
            reverse("approve-tasks-business-process", kwargs={"pk": self.object.pk}) + "?" + request.GET.urlencode()
        )
