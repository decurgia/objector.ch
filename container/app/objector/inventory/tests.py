from django.test import TestCase
from django.contrib.auth import get_user_model
import rules
from .models import Location, Object


class ObjectRuleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner1 = User.objects.create_user(
            username="owner1@objector.com", email="owner1@objector.com", password="foo"
        )
        cls.owner2 = User.objects.create_user(
            username="owner2@objector.com", email="owner2@objector.com", password="foo"
        )
        cls.object = Object.objects.create(name="object", owner=cls.owner1)

    def test_object_owner_permissions(self):
        self.assertEqual(
            rules.has_perm("inventory.view_object", self.owner1, self.object),
            True,
        )
        self.assertEqual(
            rules.has_perm("inventory.change_object", self.owner1, self.object),
            True,
        )
        self.assertEqual(
            rules.has_perm("inventory.delete_object", self.owner1, self.object),
            True,
        )

    def test_object_non_owner_permissions(self):
        self.assertEqual(
            rules.has_perm("inventory.view_object", self.owner2, self.object),
            False,
        )
        self.assertEqual(
            rules.has_perm("inventory.change_object", self.owner2, self.object),
            False,
        )
        self.assertEqual(
            rules.has_perm("inventory.delete_object", self.owner2, self.object),
            False,
        )


class LocationRuleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner1 = User.objects.create_user(
            username="owner1@objector.com", email="owner1@objector.com", password="foo"
        )
        cls.owner2 = User.objects.create_user(
            username="owner2@objector.com", email="owner2@objector.com", password="foo"
        )
        cls.location = Location.objects.create(name="location", owner=cls.owner1)

    def test_location_owner_permissions(self):
        self.assertEqual(
            rules.has_perm("inventory.view_location", self.owner1, self.location),
            True,
        )
        self.assertEqual(
            rules.has_perm("inventory.change_location", self.owner1, self.location),
            True,
        )
        self.assertEqual(
            rules.has_perm("inventory.delete_location", self.owner1, self.location),
            True,
        )

    def test_location_non_owner_permissions(self):
        self.assertEqual(
            rules.has_perm("inventory.view_location", self.owner2, self.location),
            False,
        )
        self.assertEqual(
            rules.has_perm("inventory.change_location", self.owner2, self.location),
            False,
        )
        self.assertEqual(
            rules.has_perm("inventory.delete_location", self.owner2, self.location),
            False,
        )
