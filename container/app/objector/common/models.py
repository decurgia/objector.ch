from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModelMixin


class User(RulesModelMixin, AbstractUser):
    class Languages(models.TextChoices):
        GERMAN = "de", _("German")
        ENGLISH = "en", _("English")

    send_status_report_at = models.TimeField(
        _("Send status report at"), blank=True, null=True
    )
    status_report_last_sent_at = models.DateTimeField(
        _("Status report last sent at"), blank=True, null=True
    )
    status_report_language = models.CharField(
        _("Status report language"),
        choices=Languages.choices,
        default=Languages.ENGLISH,
        max_length=2,
    )

    def get_picture(self) -> str:
        social_user = self.social_auth.get()
        picture = social_user.extra_data.get("picture", "")
        return picture

    def get_absolute_url(self) -> str:
        return f"/user/{self.id}"
