from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModel
from inventory.models import Object, Sensor
import uuid
import pathlib
from jsonpath_ng import parse


def journal_image_upload_handler(instance, filename: str) -> str:
    file_name = str(uuid.uuid1())  # uuid1 -> uuid + timestamp
    file_suffix = pathlib.Path(filename).suffix
    return f"object/{instance.object.id}/journal/{file_name}{file_suffix}"


def document_file_upload_handler(instance, filename) -> str:
    file_name = str(uuid.uuid1())  # uuid1 -> uuid + timestamp
    file_suffix = pathlib.Path(filename).suffix
    return f"object/{instance.object.id}/document/{file_name}{file_suffix}"


class Task(RulesModel):
    class Statuses(models.IntegerChoices):
        OVERDUE = 10, _("Overdue")
        DUE = 20, _("Due")
        PENDING = 30, _("Pending")
        INACTIVE = 40, _("Inactive")

    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    object = models.ForeignKey(
        Object,
        verbose_name=_("Object"),
        related_name="task_object",
        on_delete=models.CASCADE,
    )
    status = models.PositiveSmallIntegerField(
        _("Status"), choices=Statuses.choices, default=Statuses.PENDING
    )
    due_at = models.DateTimeField(_("Due at"), blank=True, null=True)
    overdue_at = models.DateTimeField(_("Overdue at"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created by"),
        related_name="task_created_by",
        on_delete=models.SET_NULL,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Updated by"),
        related_name="task_updated_by",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ["status", "overdue_at", "due_at", "updated_at"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"/task/{self.id}"

    def get_new_task_status(self) -> int:
        now = timezone.now()
        new_task_status = Task.Statuses.PENDING
        if self.overdue_at and now >= self.overdue_at:
            new_task_status = Task.Statuses.OVERDUE
        elif self.due_at and now >= self.due_at:
            new_task_status = Task.Statuses.DUE
        return new_task_status

    @property
    def status_color(self) -> str:
        status_color = "green"
        if self.status == self.Statuses.OVERDUE:
            status_color = "red"
        elif self.status == self.Statuses.DUE:
            status_color = "amber"
        elif self.status == self.Statuses.INACTIVE:
            status_color = "grey"
        return status_color


class Journal(RulesModel):
    class Sources(models.TextChoices):
        SENSOR = "sensor", _("Sensor")
        TASK = "task", _("Task")
        OBJECT = "object", _("Object")
        LOCATION = "location", _("Location")

    object = models.ForeignKey(
        Object,
        verbose_name=_("Object"),
        related_name="journal_object",
        on_delete=models.CASCADE,
    )
    notes = models.TextField(_("Notes"), blank=True)
    image = models.ImageField(
        _("Image"), upload_to=journal_image_upload_handler, blank=True, null=True
    )
    labor_costs = models.DecimalField(
        _("Labor costs"), blank=True, null=True, decimal_places=2, max_digits=9
    )
    material_costs = models.DecimalField(
        _("Material costs"), blank=True, null=True, decimal_places=2, max_digits=9
    )
    source = models.CharField(
        _("Source"), max_length=8, choices=Sources.choices, blank=True
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created by"),
        related_name="journal_created_by",
        on_delete=models.SET_NULL,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Updated by"),
        related_name="journal_updated_by",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self) -> str:
        return str(self.id)

    def get_absolute_url(self) -> str:
        return f"/journal/{self.id}"

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")
        ordering = ("-updated_at",)


class Trigger(RulesModel):
    class Conditions(models.TextChoices):
        EQUALS = "==", _("equals")
        NOTEQUALS = "!=", _("not equals")
        LESSTHAN = "<", _("less than")
        LESSTHANOREQUALTO = "<=", _("less than or equal to")
        GREATERTHAN = ">", _("greater than")
        GREATERTHANOREQUALTO = ">=", _("greater than or equal to")

    class Statuses(models.IntegerChoices):
        RED = 10, _("Alert")
        AMBER = 20, _("Warning")
        GREEN = 30, _("Normal")

    name = models.CharField(_("name"), max_length=200)
    sensor = models.ForeignKey(
        Sensor,
        verbose_name=_("Sensor"),
        related_name="trigger_sensor",
        on_delete=models.CASCADE,
    )
    jsonpath_expression = models.CharField(
        _("JSONPath expression"),
        max_length=200,
        help_text='Use <a href="http://json2jsonpath.com" target="_blank">JSONPath generator</a>'
        " with expected JSON payload.",
    )
    condition = models.CharField(
        _("Condition"), max_length=2, choices=Conditions.choices
    )
    sensor_value = models.CharField(_("Sensor value"), max_length=200, blank=True)
    amber_value = models.CharField(_("Warning value"), max_length=200, blank=True)
    red_value = models.CharField(_("Alert value"), max_length=200, blank=True)
    status = models.PositiveSmallIntegerField(
        _("Status"), choices=Statuses.choices, default=Statuses.GREEN
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created by"),
        related_name="trigger_created_by",
        on_delete=models.SET_NULL,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Updated by"),
        related_name="trigger_updated_by",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"/trigger/{self.id}"

    @property
    def status_color(self) -> str:
        status_color = "green"
        if self.status == Trigger.Statuses.RED:
            status_color = "red"
        elif self.status == Trigger.Statuses.AMBER:
            status_color = "amber"
        return status_color

    def get_trigger_sensor_value(
        self, match_value, trigger_condition: str, trigger_value: str
    ) -> str:
        trigger_sensor_value = ""
        type_matched_trigger_value = match_value

        if match_value and trigger_condition and trigger_value:
            try:
                type_matched_trigger_value = type(match_value)(trigger_value)
            except ValueError:
                trigger_sensor_value = "Error: Type mismatch. Matched value can't be compared to trigger value."

            if len(str(match_value)) > 200:
                trigger_sensor_value = (
                    "Error: Sensor value to long. Check JSONPath expression."
                )
            elif (
                (
                    Trigger.Conditions.EQUALS == trigger_condition
                    and match_value == type_matched_trigger_value
                )
                or (
                    Trigger.Conditions.NOTEQUALS == trigger_condition
                    and match_value != type_matched_trigger_value
                )
                or (
                    Trigger.Conditions.LESSTHAN == trigger_condition
                    and match_value < type_matched_trigger_value
                )
                or (
                    Trigger.Conditions.LESSTHANOREQUALTO == trigger_condition
                    and match_value <= type_matched_trigger_value
                )
                or (
                    Trigger.Conditions.GREATERTHAN == trigger_condition
                    and match_value > type_matched_trigger_value
                )
                or (
                    Trigger.Conditions.GREATERTHANOREQUALTO == trigger_condition
                    and match_value >= type_matched_trigger_value
                )
            ):
                trigger_sensor_value = str(match_value)

        return trigger_sensor_value

    def set_trigger_status_and_sensor_value(self, object_webhook_payload: str) -> None:
        trigger_status = self.Statuses.GREEN
        trigger_sensor_value = ""
        jsonpath_expression = parse(self.jsonpath_expression)

        for match in jsonpath_expression.find(object_webhook_payload):
            if trigger_status > self.Statuses.RED:
                trigger_sensor_value_red = ""
                trigger_sensor_value_red = self.get_trigger_sensor_value(
                    match.value,
                    self.condition,
                    self.red_value,
                )
                if trigger_sensor_value_red:
                    trigger_status = self.Statuses.RED
                    trigger_sensor_value = trigger_sensor_value_red

            if trigger_status > self.Statuses.AMBER:
                trigger_sensor_value_amber = ""
                trigger_sensor_value_amber = self.get_trigger_sensor_value(
                    match.value,
                    self.condition,
                    self.amber_value,
                )
                if trigger_sensor_value_amber:
                    trigger_status = self.Statuses.AMBER
                    trigger_sensor_value = trigger_sensor_value_amber

            if trigger_status == self.Statuses.GREEN:
                trigger_sensor_value = match.value

        self.status = trigger_status
        self.sensor_value = trigger_sensor_value
        self.save()


class Document(RulesModel):
    class Types(models.TextChoices):
        INSTRUCTIONS = "manual", _("Manual")
        RECEIPT = "receipt", _("Receipt")
        WARRANTY = "warranty", _("Warranty")

    object = models.ForeignKey(
        Object,
        verbose_name=_("Object"),
        related_name="document_object",
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Name"), max_length=200)
    content = models.TextField(_("Content"), blank=True)
    file = models.FileField(
        _("File"), upload_to=document_file_upload_handler, blank=True, null=True
    )
    type = models.CharField(_("Type"), max_length=8, choices=Types.choices, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created by"),
        related_name="document_created_by",
        on_delete=models.SET_NULL,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Updated by"),
        related_name="document_updated_by",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"/document/{self.id}"

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        ordering = ("-updated_at",)
