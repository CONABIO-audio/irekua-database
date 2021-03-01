import pytest

# pylint: disable=unused-wildcard-import,wildcard-import
from irekua_database.tests.fixtures.users import *
from irekua_collections.tests.fixtures.collection_types import *


@pytest.mark.django_db
def test_is_admin(collection_type_A, manager_A, manager_B, superuser):
    assert collection_type_A.is_admin(manager_A)
    assert not collection_type_A.is_admin(manager_B)
    assert not collection_type_A.is_admin(superuser)
