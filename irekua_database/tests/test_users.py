from django.db import utils
from django.test import TestCase

from irekua_database.models import User
from irekua_database.models import UserInstitution


class UserTestCase(TestCase):
    fixtures = ["irekua_database/users.json"]

    def test_user_is_special(self):
        superuser = User.objects.get(username="superuser")
        staff = User.objects.get(username="staff")
        developer = User.objects.get(username="developer")
        model = User.objects.get(username="model")
        curator = User.objects.get(username="curator")
        regular = User.objects.get(username="regular")
        inactive = User.objects.get(username="inactive")

        self.assertTrue(superuser.is_special)
        self.assertTrue(developer.is_special)
        self.assertTrue(model.is_special)
        self.assertTrue(curator.is_special)
        self.assertFalse(staff.is_special)
        self.assertFalse(regular.is_special)
        self.assertFalse(inactive.is_special)

    def test_unique_email(self):
        with self.assertRaises(utils.IntegrityError):
            User.objects.create(
                username="user1", email="user@irekua.com", password="irekua"
            )
            User.objects.create(
                username="user2", email="user@irekua.com", password="irekua"
            )
