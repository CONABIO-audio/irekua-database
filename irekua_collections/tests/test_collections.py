import pytest

from irekua_collections.models import Collection

# pytest: disable=wildcard-import
from irekua_database.tests.fixtures.users import *
from irekua_collections.tests.fixtures.data_collections import *


@pytest.mark.django_db
def test_collection_manager(
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
    external_user_A,
    closed_collection_A,
    closed_collection_B,
    open_collection_A,
):
    assert Collection.objects.open().count() == 1

    assert Collection.objects.managed(superuser).count() == 0
    assert Collection.objects.managed(curator).count() == 0
    assert Collection.objects.managed(developer).count() == 0
    assert Collection.objects.managed(manager_A).count() == 2
    assert Collection.objects.managed(manager_B).count() == 1
    assert Collection.objects.managed(administrator_A).count() == 0
    assert Collection.objects.managed(administrator_B).count() == 0
    assert Collection.objects.managed(collection_user_A).count() == 0
    assert Collection.objects.managed(collection_user_B).count() == 0
    assert Collection.objects.managed(restricted_user_A).count() == 0
    assert Collection.objects.managed(restricted_user_B).count() == 0
    assert Collection.objects.managed(external_user_A).count() == 0

    assert Collection.objects.administered(superuser).count() == 0
    assert Collection.objects.administered(curator).count() == 0
    assert Collection.objects.administered(developer).count() == 0
    assert Collection.objects.administered(manager_A).count() == 0
    assert Collection.objects.administered(manager_B).count() == 0
    assert Collection.objects.administered(administrator_A).count() == 1
    assert Collection.objects.administered(administrator_B).count() == 1
    assert Collection.objects.administered(collection_user_A).count() == 0
    assert Collection.objects.administered(collection_user_B).count() == 0
    assert Collection.objects.administered(restricted_user_A).count() == 0
    assert Collection.objects.administered(restricted_user_B).count() == 0
    assert Collection.objects.administered(external_user_A).count() == 0

    assert Collection.objects.user(superuser).count() == 0
    assert Collection.objects.user(curator).count() == 0
    assert Collection.objects.user(developer).count() == 0
    assert Collection.objects.user(manager_A).count() == 0
    assert Collection.objects.user(manager_B).count() == 0
    assert Collection.objects.user(administrator_A).count() == 0
    assert Collection.objects.user(administrator_B).count() == 0
    assert Collection.objects.user(collection_user_A).count() == 1
    assert Collection.objects.user(collection_user_B).count() == 1
    assert Collection.objects.user(restricted_user_A).count() == 1
    assert Collection.objects.user(restricted_user_B).count() == 1
    assert Collection.objects.user(external_user_A).count() == 0

    assert Collection.objects.can_view(superuser).count() == 3
    assert Collection.objects.can_view(curator).count() == 3
    assert Collection.objects.can_view(developer).count() == 3
    assert Collection.objects.can_view(manager_A).count() == 2
    assert Collection.objects.can_view(manager_B).count() == 2
    assert Collection.objects.can_view(administrator_A).count() == 2
    assert Collection.objects.can_view(administrator_B).count() == 2
    assert Collection.objects.can_view(collection_user_A).count() == 2
    assert Collection.objects.can_view(collection_user_B).count() == 2
    assert Collection.objects.can_view(restricted_user_A).count() == 2
    assert Collection.objects.can_view(restricted_user_B).count() == 2
    assert Collection.objects.can_view(external_user_A).count() == 1


@pytest.mark.django_db
def test_collection_can_view(
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
    external_user_A,
    closed_collection_A,
    closed_collection_B,
    open_collection_A,
):

    assert closed_collection_A.can_view(superuser)
    assert closed_collection_A.can_view(curator)
    assert closed_collection_A.can_view(developer)
    assert closed_collection_A.can_view(manager_A)
    assert not closed_collection_A.can_view(manager_B)
    assert closed_collection_A.can_view(administrator_A)
    assert not closed_collection_A.can_view(administrator_B)
    assert closed_collection_A.can_view(collection_user_A)
    assert not closed_collection_A.can_view(collection_user_B)
    assert closed_collection_A.can_view(restricted_user_A)
    assert not closed_collection_A.can_view(restricted_user_B)
    assert not closed_collection_A.can_view(external_user_A)

    assert closed_collection_B.can_view(superuser)
    assert closed_collection_B.can_view(curator)
    assert closed_collection_B.can_view(developer)
    assert not closed_collection_B.can_view(manager_A)
    assert closed_collection_B.can_view(manager_B)
    assert not closed_collection_B.can_view(administrator_A)
    assert closed_collection_B.can_view(administrator_B)
    assert not closed_collection_B.can_view(collection_user_A)
    assert closed_collection_B.can_view(collection_user_B)
    assert not closed_collection_B.can_view(restricted_user_A)
    assert closed_collection_B.can_view(restricted_user_B)
    assert not closed_collection_B.can_view(external_user_A)

    assert open_collection_A.can_view(superuser)
    assert open_collection_A.can_view(curator)
    assert open_collection_A.can_view(developer)
    assert open_collection_A.can_view(manager_A)
    assert open_collection_A.can_view(manager_B)
    assert open_collection_A.can_view(administrator_A)
    assert open_collection_A.can_view(administrator_B)
    assert open_collection_A.can_view(collection_user_A)
    assert open_collection_A.can_view(collection_user_B)
    assert open_collection_A.can_view(restricted_user_A)
    assert open_collection_A.can_view(restricted_user_B)
    assert open_collection_A.can_view(external_user_A)
