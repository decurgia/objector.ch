from .models import Location, Object, Sensor
import django_filters


def get_location_queryset(request):
    groups = request.user.groups.values_list("pk", flat=True)
    groups_as_list = list(groups)
    queryset = (
        Location.objects.filter(owner=request.user)
        | Location.objects.filter(management_group__in=groups_as_list)
        | Location.objects.filter(maintenance_group__in=groups_as_list)
    )
    return queryset


def get_object_queryset(request):
    groups = request.user.groups.values_list("pk", flat=True)
    groups_as_list = list(groups)
    queryset = (
        Object.objects.filter(owner=request.user)
        | Object.objects.filter(management_group__in=groups_as_list)
        | Object.objects.filter(maintenance_group__in=groups_as_list)
    )
    return queryset


class LocationFilter(django_filters.FilterSet):
    class Meta:
        model = Location
        fields = ["status"]


class ObjectFilter(django_filters.FilterSet):
    location = django_filters.filters.ModelChoiceFilter(queryset=get_location_queryset)

    class Meta:
        model = Object
        fields = ["location", "status"]


class SensorFilter(django_filters.FilterSet):
    object__location = django_filters.filters.ModelChoiceFilter(
        queryset=get_location_queryset
    )
    object = django_filters.filters.ModelChoiceFilter(queryset=get_object_queryset)

    class Meta:
        model = Sensor
        fields = ["object__location", "object", "status"]
