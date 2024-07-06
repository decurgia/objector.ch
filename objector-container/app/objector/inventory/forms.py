from django import forms
from .models import Location, Object, Sensor


class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = [
            "location",
            "name",
            "description",
            "owner",
            "management_group",
            "maintenance_group",
        ]

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        location_queryset = Location.objects.filter(
            owner=self.request.user
        ) | Location.objects.filter(management_group__in=groups_as_list)

        self.fields["location"].queryset = location_queryset


class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = [
            "object",
            "name",
            "description",
            "image",
        ]

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        # all groups for user
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        object_queryset = Object.objects.filter(
            owner=self.request.user
        ) | Object.objects.filter(management_group__in=groups_as_list)

        self.fields["object"].queryset = object_queryset
