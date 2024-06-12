from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    RedirectView,
    UpdateView,
    DetailView,
    DeleteView,
    TemplateView,
)
from django.db.models import Min, Max
from inventory.models import Location
from maintenance.models import Task
from inventory.models import Sensor
from django.utils import timezone
from rules.contrib.views import AutoPermissionRequiredMixin
from .models import User
from .forms import UserForm
from django.urls import reverse_lazy


class HomeTemplateView(TemplateView):
    template_name = "common/home.html"


class LogoutRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs) -> str:
        django_logout(self.request)
        domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
        client_id = settings.SOCIAL_AUTH_AUTH0_KEY
        return_to = self.request.build_absolute_uri("/")
        return f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}"


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "common/dashboard.html"

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        groups = self.request.user.groups.values_list("pk", flat=True)
        groups_as_list = list(groups)
        overdue_tasks_queryset = (
            Task.objects.filter(
                object__owner=self.request.user, status=Task.Statuses.OVERDUE
            )
            | Task.objects.filter(
                object__management_group__in=groups_as_list,
                status=Task.Statuses.OVERDUE,
            )
            | Task.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Task.Statuses.OVERDUE,
            )
        )
        due_tasks_queryset = (
            Task.objects.filter(
                object__owner=self.request.user, status=Task.Statuses.DUE
            )
            | Task.objects.filter(
                object__management_group__in=groups_as_list,
                status=Task.Statuses.DUE,
            )
            | Task.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Task.Statuses.DUE,
            )
        )
        pending_tasks_queryset = (
            Task.objects.filter(
                object__owner=self.request.user, status=Task.Statuses.PENDING
            )
            | Task.objects.filter(
                object__management_group__in=groups_as_list,
                status=Task.Statuses.PENDING,
            )
            | Task.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Task.Statuses.PENDING,
            )
        )
        red_sensors_queryset = (
            Sensor.objects.filter(
                object__owner=self.request.user, status=Sensor.Statuses.RED
            )
            | Sensor.objects.filter(
                object__management_group__in=groups_as_list, status=Sensor.Statuses.RED
            )
            | Sensor.objects.filter(
                object__maintenance_group__in=groups_as_list, status=Sensor.Statuses.RED
            )
        )
        amber_sensors_queryset = (
            Sensor.objects.filter(
                object__owner=self.request.user, status=Sensor.Statuses.AMBER
            )
            | Sensor.objects.filter(
                object__management_group__in=groups_as_list,
                status=Sensor.Statuses.AMBER,
            )
            | Sensor.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Sensor.Statuses.AMBER,
            )
        )
        green_sensors_queryset = (
            Sensor.objects.filter(
                object__owner=self.request.user, status=Sensor.Statuses.GREEN
            )
            | Sensor.objects.filter(
                object__management_group__in=groups_as_list,
                status=Sensor.Statuses.GREEN,
            )
            | Sensor.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Sensor.Statuses.GREEN,
            )
        )
        location_queryset = (
            Location.objects.filter(
                owner=self.request.user, latitude__isnull=False, longitude__isnull=False
            )
            | Location.objects.filter(
                management_group__in=groups_as_list,
                latitude__isnull=False,
                longitude__isnull=False,
            )
            | Location.objects.filter(
                maintenance_group__in=groups_as_list,
                latitude__isnull=False,
                longitude__isnull=False,
            )
        )
        context["overdue_tasks_count"] = overdue_tasks_queryset.count()
        context["due_tasks_count"] = due_tasks_queryset.count()
        context["pending_tasks_count"] = pending_tasks_queryset.count()
        context["red_sensors_count"] = red_sensors_queryset.count()
        context["amber_sensors_count"] = amber_sensors_queryset.count()
        context["green_sensors_count"] = green_sensors_queryset.count()
        context["locations"] = location_queryset
        context["locations_aggregates"] = location_queryset.aggregate(
            Min("latitude"), Max("latitude"), Min("longitude"), Max("longitude")
        )
        context["current_datetime"] = timezone.now()

        return context


class UserDetailView(AutoPermissionRequiredMixin, DetailView):
    model = User
    raise_exception = True


class UserUpdateView(AutoPermissionRequiredMixin, UpdateView):
    model = User
    raise_exception = True
    form_class = UserForm


class UserDeleteView(AutoPermissionRequiredMixin, DeleteView):
    model = User
    raise_exception = True
    success_url = reverse_lazy("home")
