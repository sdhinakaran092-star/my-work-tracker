from django import forms

from .models import PendingWork


class PendingWorkForm(forms.ModelForm):
    class Meta:
        model = PendingWork
        fields = ["title", "description", "due_at", "to_email"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "(optional)"}
            ),
            "due_at": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "to_email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "(optional)"}
            ),
        }

    def clean_due_at(self):
        value = self.cleaned_data.get("due_at")
        return value
