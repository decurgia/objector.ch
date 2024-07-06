from django.db import models
from django.conf import settings
from rules.contrib.models import RulesModel
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


def location_image_upload_handler(instance, filename) -> str:
    return f"location/{instance.id}/image/{filename}"


def object_image_upload_handler(instance, filename) -> str:
    return f"object/{instance.id}/image/{filename}"


class Location(RulesModel):
    class Statuses(models.IntegerChoices):
        RED = 10, _("Alert")
        AMBER = 20, _("Warning")
        GREEN = 30, _("Normal")

    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    image = models.ImageField(
        _("Image"), upload_to=location_image_upload_handler, blank=True, null=True
    )
    address = models.TextField(_("Address"), blank=True)
    latitude = models.FloatField(_("Latitude"), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        _("Status"), choices=Statuses.choices, default=Statuses.GREEN
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Owner"),
        related_name="location_owner",
        on_delete=models.CASCADE,
        help_text=_("Owner can view, change or delete this location."),
    )
    management_group = models.ForeignKey(
        Group,
        verbose_name=_("Management group"),
        related_name="location_management_group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Group members can view, change or delete this location."),
    )
    maintenance_group = models.ForeignKey(
        Group,
        verbose_name=_("Maintenance group"),
        related_name="location_maintenance_group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Group members can view this location."),
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created by"),
        related_name="location_created_by",
        on_delete=models.SET_NULL,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Updated by"),
        related_name="location_updated_by",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["status", "name"]
        indexes = [
            models.Index(fields=["owner", "management_group", "maintenance_group"]),
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"/location/{self.id}"

    @property
    def status_color(self) -> str:
        status_color = "green"
        if self.status == self.Statuses.RED:
            status_color = "red"
        elif self.status == self.Statuses.AMBER:
            status_color = "amber"
        return status_color


class Object(RulesModel):
    class Statuses(models.IntegerChoices):
        RED = 10, _("Alert")
        AMBER = 20, _("Warning")
        GREEN = 30, _("Normal")

    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    image = models.ImageField(
        _("Image"), upload_to=object_image_upload_handler, blank=True, null=True
    )
    location = models.ForeignKey(
        Location,
        verbose_name=_("Location"),
        related_name="object_location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    status = models.PositiveSmallIntegerField(
        _("Status"), choices=Statuses.choices, default=Statuses.GREEN
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Owner"),
        related_name="object_owner",
        on_delete=models.CASCADE,
        help_text=_("Owner can view, change or delete this object."),
    )
    management_group = models.ForeignKey(
        Group,
        verbose_name=_("Management group"),
        related_name="object_management_group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Group members can view or update this object."),
    )
    maintenance_group = models.ForeignKey(
        Group,
        verbose_name=_("Maintenance group"),
        related_name="object_maintenance_group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Group members can view this object."),
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created by"),
        related_name="object_created_by",
        on_delete=models.SET_NULL,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Updated by"),
        related_name="object_updated_by",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = _("Object")
        verbose_name_plural = _("Objects")
        ordering = ["status", "name"]
        indexes = [
            models.Index(fields=["owner", "management_group", "maintenance_group"]),
        ]

    def __str__(self) -> str:
        str = self.name
        if self.location:
            str = f"{str} @{self.location}"
        return str

    def get_absolute_url(self) -> str:
        return f"/object/{self.id}"

    @property
    def status_color(self) -> str:
        status_color = "green"
        if self.status == self.Statuses.RED:
            status_color = "red"
        elif self.status == self.Statuses.AMBER:
            status_color = "amber"
        return status_color


class Sensor(RulesModel):
    class Statuses(models.IntegerChoices):
        RED = 10, _("Alert")
        AMBER = 20, _("Warning")
        GREEN = 30, _("Normal")

    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    image = models.ImageField(
        _("Image"), upload_to=object_image_upload_handler, blank=True, null=True
    )
    object = models.ForeignKey(
        Object,
        verbose_name=_("Object"),
        related_name="sensor_object",
        on_delete=models.CASCADE,
    )
    status = models.PositiveSmallIntegerField(
        _("Status"), choices=Statuses.choices, default=Statuses.GREEN
    )
    webhook_authorization = models.CharField(
        _("Webhook authorization"), max_length=255, blank=True
    )
    webhook_payload = models.JSONField(_("Webhook payload"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created by"),
        related_name="sensor_created_by",
        on_delete=models.SET_NULL,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Updated by"),
        related_name="sensor_updated_by",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = _("Sensor")
        verbose_name_plural = _("Sensors")
        ordering = ["status", "name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"/sensor/{self.id}"

    def save(self, *args, **kwargs):
        self.set_sensor_status()
        super().save(*args, **kwargs)

    def set_sensor_status(self) -> None:
        sensor_status = self.Statuses.GREEN

        from maintenance.models import Trigger

        triggers = Trigger.objects.filter(sensor=self.id)

        for trigger in triggers:
            trigger.set_trigger_status_and_sensor_value(self.webhook_payload)

            if sensor_status > trigger.status:
                sensor_status = trigger.status

        self.status = sensor_status

    @property
    def status_color(self) -> str:
        status_color = "green"
        if self.status == self.Statuses.RED:
            status_color = "red"
        elif self.status == self.Statuses.AMBER:
            status_color = "amber"
        return status_color
