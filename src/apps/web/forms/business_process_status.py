from django import forms

from apps.tasks.models import TaskStatus, TaskColumn


class TaskStatusForm(forms.ModelForm):
    required_task_columns = forms.ModelMultipleChoiceField(
        queryset=TaskColumn.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = TaskStatus
        fields = (
            "status_name",
            "required_task_columns",
        )
        widgets = {
            "status_name": forms.TextInput(attrs={"class": "form-control"}),
            "required_task_columns": forms.SelectMultiple(attrs={"class": "form-control"}),
        }
