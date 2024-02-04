from django import forms

from apps.tasks.models import BusinessProcess


class BusinessProcessForm(forms.ModelForm):
    class Meta:
        model = BusinessProcess
        fields = (
            "title",
            "description",
            "excel_file",
            "min_bpm_group",
            "dgd_code_column",
            "dgd_name_column",
            "ugd_code_column",
        )
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "excel_file": forms.FileInput(attrs={"class": "form-control"}),
            "min_bpm_group": forms.Select(attrs={"class": "form-control"}),
            "dgd_code_column": forms.Select(attrs={"class": "form-control"}),
            "dgd_name_column": forms.Select(attrs={"class": "form-control"}),
            "ugd_code_column": forms.Select(attrs={"class": "form-control"}),
        }
