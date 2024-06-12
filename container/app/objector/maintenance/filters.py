from .models import Task, Journal
import django_filters
from inventory.models import Location, Object


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


class TaskFilter(django_filters.FilterSet):
    object__location = django_filters.filters.ModelChoiceFilter(
        queryset=get_location_queryset
    )
    object = django_filters.filters.ModelChoiceFilter(queryset=get_object_queryset)

    class Meta:
        model = Task
        fields = ["object__location", "object", "status"]


class JournalFilter(django_filters.FilterSet):
    object__location = django_filters.filters.ModelChoiceFilter(
        queryset=get_location_queryset
    )
    object = django_filters.filters.ModelChoiceFilter(queryset=get_object_queryset)

    class Meta:
        model = Journal
        fields = ["object__location", "object", "source"]
