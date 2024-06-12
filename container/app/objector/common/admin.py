from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            _("Custom Fields"),
            {
                "fields": (
                    "send_status_report_at",
                    "status_report_last_sent_at",
                    "status_report_language",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
