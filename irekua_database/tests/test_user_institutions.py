from django.db import utils
from django.test import TestCase

from irekua_database.models import User
from irekua_database.models import Institution
from irekua_database.models import UserInstitution


class UserInstitutionTestCase(TestCase):
    fixtures = ['irekua_database/users.json', 'irekua_database/institutions.json']

    def test_unique_together_user_institution(self):
        regular = User.objects.get(username='regular')
        irekua = Institution.objects.get(institution_code='irekua')

        UserInstitution.objects.create(
            user=regular,
            institution=irekua,
            position='manager')

        with self.assertRaises(utils.IntegrityError):
            UserInstitution.objects.create(
                user=regular,
                institution=irekua,
                position='ceo')
