from django.core.management.base import BaseCommand
from maintenance.models import Task


class Command(BaseCommand):
    help = "Sets the status of all task records"

    def handle(self, *args, **options):
        task_records = Task.objects.all()
        for task in task_records:
            new_task_status = Task.get_new_task_status(task)

            if task.status != new_task_status:
                task.status = new_task_status
                task.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully updated task record "{0}" status to "{1}"'
                    ).format(task.id, task.status)
                )
