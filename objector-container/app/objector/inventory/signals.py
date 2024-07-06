from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from maintenance.models import Task
from .models import Location, Object, Sensor


@receiver(post_save, sender=Object)
def object_post_save_receiver(sender, instance, created, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    if instance.location:
        transaction.on_commit(lambda: update_location_status(instance.location.id))


@receiver(post_save, sender=Task)
def task_post_save_receiver(sender, instance, created, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    transaction.on_commit(lambda: update_object_status(instance.object.id))


@receiver(post_delete, sender=Task)
def task_post_delete_receiver(sender, instance, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    transaction.on_commit(lambda: update_object_status(instance.object.id))


@receiver(post_save, sender=Sensor)
def sensor_post_save_receiver(sender, instance, created, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    transaction.on_commit(lambda: update_object_status(instance.object.id))


@receiver(post_delete, sender=Sensor)
def sensor_post_delete_receiver(sender, instance, **kwargs):
    # TODO: Use celery for async operation: https://docs.djangoproject.com/en/3.2/topics/db/transactions/
    transaction.on_commit(lambda: update_object_status(instance.object.id))


def update_location_status(location_id):
    location = Location.objects.get(id=location_id)

    new_location_status = Location.Statuses.GREEN
    if Object.objects.filter(location=location_id, status=Object.Statuses.RED).exists():
        new_location_status = Location.Statuses.RED
    elif Object.objects.filter(
        location=location_id, status=Object.Statuses.AMBER
    ).exists():
        new_location_status = Location.Statuses.AMBER

    if location.status != new_location_status:
        location.status = new_location_status
        location.save()


def update_object_status(object_id):
    object = Object.objects.get(id=object_id)
    new_object_status = Object.Statuses.GREEN

    if (
        Task.objects.filter(object=object_id, status=Task.Statuses.OVERDUE).exists()
        or Sensor.objects.filter(object=object_id, status=Sensor.Statuses.RED).exists()
    ):
        new_object_status = Object.Statuses.RED
    elif (
        Task.objects.filter(object=object_id, status=Task.Statuses.DUE).exists()
        or Sensor.objects.filter(
            object=object_id, status=Sensor.Statuses.AMBER
        ).exists()
    ):
        new_object_status = Object.Statuses.AMBER

    if object.status != new_object_status:
        object.status = new_object_status
        object.save()
