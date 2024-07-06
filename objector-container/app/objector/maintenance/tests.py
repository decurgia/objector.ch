from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import rules
from .models import Task
from inventory.models import Object


class taskRuleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner1 = User.objects.create_user(
            username="owner1@objector.com", email="owner1@objector.com", password="foo"
        )
        cls.owner2 = User.objects.create_user(
            username="owner2@objector.com", email="owner2@objector.com", password="foo"
        )
        cls.object = Object.objects.create(name="Object", owner=cls.owner1)
        cls.task = Task.objects.create(
            name="Task", object=cls.object, due_at=timezone.now()
        )

    def test_task_object_owner_permissions(self):
        self.assertEqual(
            rules.has_perm("maintenance.view_task", self.owner1, self.task),
            True,
        )
        self.assertEqual(
            rules.has_perm("maintenance.change_task", self.owner1, self.task),
            True,
        )
        self.assertEqual(
            rules.has_perm("maintenance.delete_task", self.owner1, self.task),
            True,
        )

    def test_task_object_non_owner_permissions(self):
        self.assertEqual(
            rules.has_perm("maintenance.view_task", self.owner2, self.task),
            False,
        )
        self.assertEqual(
            rules.has_perm("maintenance.change_task", self.owner2, self.task),
            False,
        )
        self.assertEqual(
            rules.has_perm("maintenance.delete_task", self.owner2, self.task),
            False,
        )
