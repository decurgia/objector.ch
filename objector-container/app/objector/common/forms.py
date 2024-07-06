from django import forms
from .models import User
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "send_status_report_at",
            "status_report_language",
        ]

    send_status_report_at = forms.TimeField(
        label=_("Send status report at"),
        required=False,
        input_formats=["%H:%M"],
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "placeholder": "Select a time",
            },
            format="%H:%M",
        ),
    )
