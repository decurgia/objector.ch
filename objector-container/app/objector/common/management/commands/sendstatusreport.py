from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
from maintenance.models import Task, Trigger
from inventory.models import Sensor
from django.utils import translation, timezone, formats
import markdown


class Command(BaseCommand):
    help = "Sends status report"

    def handle(self, *args, **options) -> None:
        self.get_users()

    def get_users(self) -> None:
        User = get_user_model()
        now = timezone.localtime()
        current_time = now.time()
        today = now.date()
        users = User.objects.filter(
            email__isnull=False,
            status_report_last_sent_at__date__lt=today,
            send_status_report_at__lt=current_time,
        ) | User.objects.filter(
            email__isnull=False,
            status_report_last_sent_at__isnull=True,
            send_status_report_at__lt=current_time,
        )
        for user in users:
            groups = user.groups.values_list("pk", flat=True)
            groups_as_list = list(groups)
            translation.activate(user.status_report_language)
            self.send_status_report(user, groups_as_list)
            user.status_report_last_sent_at = now
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Status report sent to {user}"))

    def send_status_report(self, user, groups_as_list) -> None:
        subject, from_email, to = (
            _("Status report") + " " + formats.localize(timezone.localtime()),
            "info@objector.app",
            user.email,
        )

        overdue_tasks = self.get_overdue_tasks(user, groups_as_list)
        due_tasks = self.get_due_tasks(user, groups_as_list)
        red_sensors = self.get_red_sensors(user, groups_as_list)
        amber_sensors = self.get_amber_sensors(user, groups_as_list)

        text_content = ""
        text_content += (
            f"{_('Tasks')}: {overdue_tasks.get('count', 0)} {_('Overdue')},"
            f" {due_tasks.get('count', 0)} {_('Due')}\n\n"
        )
        text_content += (
            f"{_('Sensors')}: {red_sensors.get('count', 0)} {_('Alert')},"
            f" {amber_sensors.get('count', 0)} {_('Warning')}\n\n"
        )
        if overdue_tasks.get("count", 0) > 0 or due_tasks.get("count", 0) > 0:
            text_content += f"## {_('Tasks')}\n"
        text_content += overdue_tasks.get("content", "")
        text_content += due_tasks.get("content", "")
        if red_sensors.get("count", 0) > 0 or amber_sensors.get("count", 0) > 0:
            text_content += f"## {_('Sensors')}\n"
        text_content += red_sensors.get("content", "")
        text_content += amber_sensors.get("content", "")

        text_content += "\n\n[Objector](https://objector.app)"
        html_content = markdown.markdown(text_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get_overdue_tasks(self, user, groups_as_list) -> dict:
        overdue_tasks = {}
        overdue_tasks["content"] = ""
        overdue_tasks["count"] = 0
        overdue_tasks_queryset = (
            Task.objects.filter(object__owner=user, status=Task.Statuses.OVERDUE)
            | Task.objects.filter(
                object__management_group__in=groups_as_list,
                status=Task.Statuses.OVERDUE,
            )
            | Task.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Task.Statuses.OVERDUE,
            )
        )
        if overdue_tasks_queryset:
            overdue_tasks["content"] = f"\n## {_('Overdue')}\n\n"
            for task in overdue_tasks_queryset:
                overdue_tasks["content"] += self.compile_task_content(task)
                overdue_tasks["count"] += 1

        return overdue_tasks

    def get_due_tasks(self, user, groups_as_list) -> dict:
        due_tasks = {}
        due_tasks["content"] = ""
        due_tasks["count"] = 0
        due_tasks_queryset = (
            Task.objects.filter(object__owner=user, status=Task.Statuses.DUE)
            | Task.objects.filter(
                object__management_group__in=groups_as_list,
                status=Task.Statuses.DUE,
            )
            | Task.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Task.Statuses.DUE,
            )
        )
        if due_tasks_queryset:
            due_tasks["content"] = f"\n## {_('Due')}\n\n"
            for task in due_tasks_queryset:
                due_tasks["content"] += self.compile_task_content(task)
                due_tasks["count"] += 1

        return due_tasks

    def get_red_sensors(self, user, groups_as_list):
        red_sensors = {}
        red_sensors["content"] = ""
        red_sensors["count"] = 0
        red_sensors_queryset = (
            Sensor.objects.filter(object__owner=user, status=Sensor.Statuses.RED)
            | Sensor.objects.filter(
                object__management_group__in=groups_as_list, status=Sensor.Statuses.RED
            )
            | Sensor.objects.filter(
                object__maintenance_group__in=groups_as_list, status=Sensor.Statuses.RED
            )
        )
        if red_sensors_queryset:
            red_sensors["content"] = f"\n## {_('Alert')}\n\n"
            for sensor in red_sensors_queryset:
                red_sensors["content"] += self.compile_sensor_content(sensor)
                red_sensors["count"] += 1

                red_sensor_triggers_queryset = Trigger.objects.filter(sensor=sensor)
                if red_sensor_triggers_queryset:
                    for trigger in red_sensor_triggers_queryset:
                        red_sensors["content"] += self.compile_trigger_content(trigger)
            red_sensors["content"] += "---\n"

        return red_sensors

    def get_amber_sensors(self, user, groups_as_list):
        amber_sensors = {}
        amber_sensors["content"] = ""
        amber_sensors["count"] = 0
        amber_sensors_queryset = (
            Sensor.objects.filter(object__owner=user, status=Sensor.Statuses.AMBER)
            | Sensor.objects.filter(
                object__management_group__in=groups_as_list,
                status=Sensor.Statuses.AMBER,
            )
            | Sensor.objects.filter(
                object__maintenance_group__in=groups_as_list,
                status=Sensor.Statuses.AMBER,
            )
        )
        if amber_sensors_queryset:
            amber_sensors["content"] = f"\n## {_('Warning')}\n\n"
            for sensor in amber_sensors_queryset:
                amber_sensors["content"] += self.compile_sensor_content(sensor)
                amber_sensors["count"] += 1

                amber_sensor_triggers_queryset = Trigger.objects.filter(sensor=sensor)
                if amber_sensor_triggers_queryset:
                    for trigger in amber_sensor_triggers_queryset:
                        amber_sensors["content"] += self.compile_trigger_content(
                            trigger
                        )
            amber_sensors["content"] += "---\n"

        return amber_sensors

    def compile_task_content(self, task) -> str:
        sensor_content = ""
        sensor_content += f"+ {_('Task')}: [{task.name}](https://{settings.DEFAULT_HOST}/task/{task.pk}/)\n"
        sensor_content += (
            f"+ {_('Object')}: "
            f"[{task.object}](https://{settings.DEFAULT_HOST}/object/{task.object.pk}/)\n"
        )
        if task.object.location:
            sensor_content += (
                f"+ {_('Location')}: "
                f"[{task.object.location}](https://{settings.DEFAULT_HOST}/location/{task.object.location.pk}/)\n"
            )
        sensor_content += f"+ {_('Due at')}: {formats.localize(task.due_at)}\n"
        sensor_content += f"+ {_('Overdue at')}: {formats.localize(task.overdue_at)}\n"
        sensor_content += "---\n"

        return sensor_content

    def compile_sensor_content(self, sensor) -> str:
        sensor_content = ""
        sensor_content += f"### {_('Sensor')} [{sensor.name}](https:/{settings.DEFAULT_HOST}/sensor/{sensor.pk}/)\n"
        sensor_content += (
            f"+ {_('Object')}: "
            f"[{sensor.object}](https://{settings.DEFAULT_HOST}/object/{sensor.object.pk}/)\n"
        )
        if sensor.object.location:
            sensor_content += (
                f"+ {_('Location')}: "
                f"[{sensor.object.location}](https://{settings.DEFAULT_HOST}/location/{sensor.object.location.pk}/)\n"
            )
        sensor_content += (
            f"+ {_('Updated at')}: {formats.localize(sensor.updated_at)}\n"
        )

        return sensor_content

    def compile_trigger_content(self, trigger) -> str:
        trigger_content = ""
        trigger_content += f"#### {_('Trigger')}" \
            f" [{trigger.name}](https://{settings.DEFAULT_HOST}/trigger/{trigger.pk}/)\n"
        trigger_content += f"+ {_('Sensor value')}: {trigger.sensor_value}\n"
        trigger_content += f"+ {_('Condition')}: {trigger.get_condition_display()}\n"
        if trigger.amber_value:
            trigger_content += f"+ {_('Warning value')}: {trigger.amber_value}\n"
        if trigger.red_value:
            trigger_content += f"+ {_('Alert value')}: {trigger.red_value}\n"
        trigger_content += f"+ {_('Status')}: {trigger.get_status_display()}\n"
        trigger_content += (
            f"+ {_('Updated at')}: {formats.localize(trigger.updated_at)}\n"
        )

        return trigger_content
