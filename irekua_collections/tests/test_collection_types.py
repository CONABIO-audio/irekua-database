import pytest

# pylint: disable=unused-wildcard-import,wildcard-import
from irekua_database.tests.fixtures.users import *
from irekua_collections.tests.fixtures.collection_types import *


@pytest.mark.django_db
def test_is_admin(collection_type_A, manager_A, manager_B, superuser):
    assert collection_type_A.is_admin(manager_A)
    assert not collection_type_A.is_admin(manager_B)
    assert not collection_type_A.is_admin(superuser)


@pytest.mark.django_db
def test_can_create_collection(
    collection_type_A,
    superuser,
    curator,
    developer,
    manager_A,
    manager_B,
    administrator_A,
    administrator_B,
    collection_user_A,
    collection_user_B,
    restricted_user_A,
    restricted_user_B,
):
    assert collection_type_A.can_create_collection(superuser)
    assert not collection_type_A.can_create_collection(curator)
    assert not collection_type_A.can_create_collection(developer)
    assert collection_type_A.can_create_collection(manager_A)
    assert not collection_type_A.can_create_collection(manager_B)
    assert not collection_type_A.can_create_collection(administrator_A)
    assert not collection_type_A.can_create_collection(administrator_B)
    assert not collection_type_A.can_create_collection(collection_user_A)
    assert not collection_type_A.can_create_collection(collection_user_B)
    assert not collection_type_A.can_create_collection(restricted_user_A)
    assert not collection_type_A.can_create_collection(restricted_user_B)
