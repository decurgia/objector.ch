from django import forms
from .models import Task, Journal, Document
from inventory.models import Object


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "object",
            "name",
            "description",
            "due_at",
            "overdue_at",
            "status",
        ]

    due_at = forms.DateTimeField(
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "placeholder": "Select a due date and time",
            },
            format="%Y-%m-%dT%H:%M",
        ),
    )
    overdue_at = forms.DateTimeField(
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "placeholder": "Select an overdue date and time",
            },
            format="%Y-%m-%dT%H:%M",
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        object_queryset = (
            Object.objects.filter(owner=self.request.user)
            | Object.objects.filter(management_group__in=groups_as_list)
            | Object.objects.filter(maintenance_group__in=groups_as_list)
        )

        self.fields["object"].queryset = object_queryset


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["object", "notes", "image", "labor_costs", "material_costs"]

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        object_queryset = (
            Object.objects.filter(owner=self.request.user)
            | Object.objects.filter(management_group__in=groups_as_list)
            | Object.objects.filter(maintenance_group__in=groups_as_list)
        )

        self.fields["object"].queryset = object_queryset


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            "object",
            "name",
            "content",
            "file",
            "type",
        ]

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        object_queryset = (
            Object.objects.filter(owner=self.request.user)
            | Object.objects.filter(management_group__in=groups_as_list)
            | Object.objects.filter(maintenance_group__in=groups_as_list)
        )

        self.fields["object"].queryset = object_queryset
