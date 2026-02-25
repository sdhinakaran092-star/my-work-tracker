from django import forms

from .models import WorkStatus


class WorkStatusForm(forms.ModelForm):
    class Meta:
        model = WorkStatus
        fields = ["work_done"]
        widgets = {
            "work_done": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                    "placeholder": "What did you work on today?",
                }
            ),
        }
