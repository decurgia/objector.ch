from django.contrib import admin
from .models import Task, Journal, Trigger


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "object", "status", "due_at", "overdue_at")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")


class JournalAdmin(admin.ModelAdmin):
    list_display = ("object", "notes", "labor_costs", "material_costs")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")


class TriggerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sensor",
        "status",
        "sensor_value",
        "condition",
        "amber_value",
        "red_value",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )


admin.site.register(Task, TaskAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Trigger, TriggerAdmin)
