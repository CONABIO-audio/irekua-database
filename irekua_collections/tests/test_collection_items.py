import pytest

from irekua_collections.models import CollectionItem

# pylint: disable=unused-wildcard-import,wildcard-import
from irekua_database.tests.fixtures.users import *
from irekua_items.tests.fixtures.mime_types import *
from irekua_items.tests.fixtures.item_types import *
from irekua_collections.tests.fixtures.collection_items import *
from irekua_collections.tests.fixtures.data_collections import *


@pytest.mark.django_db
def test_can_view(
    collection_item_factory,
    superuser,
    developer,
    curator,
    manager_A,
    manager_B,
    administrator_A,
    administrator_B,
    closed_collection_A,
    closed_collection_B,
    collection_user_A,
    collection_user_B,
    restricted_user_A,
    restricted_user_B,
    external_user_A,
    restrictive_licence,
    inactive_restrictive_licence,
    unrestrictive_licence,
):
    collection = closed_collection_A

    assert collection.collection_type.is_admin(manager_A)
    assert collection.is_admin(administrator_A)
    assert collection.is_user(collection_user_A)
    assert collection.is_user(restricted_user_A)
    assert not collection.collection_type.is_admin(manager_B)
    assert not collection.is_admin(administrator_B)
    assert not collection.is_user(collection_user_B)
    assert not collection.is_user(restricted_user_B)
    assert not collection.is_user(external_user_A)

    # Item created by collection user
    # with restricted licence
    item1 = collection_item_factory(
        collection=collection,
        created_by=collection_user_A,
        licence=restrictive_licence,
    )

    assert item1.can_view(superuser)
    assert item1.can_view(curator)
    assert item1.can_view(developer)
    assert item1.can_view(manager_A)
    assert item1.can_view(administrator_A)
    assert item1.can_view(collection_user_A)
    assert not item1.can_view(manager_B)
    assert not item1.can_view(administrator_B)
    assert not item1.can_view(restricted_user_A)
    assert not item1.can_view(collection_user_B)
    assert not item1.can_view(restricted_user_B)
    assert not item1.can_view(external_user_A)

    # Item created by restricted user
    # with restricted licence
    item2 = collection_item_factory(
        collection=collection,
        created_by=restricted_user_A,
        licence=restrictive_licence,
    )

    assert item2.can_view(superuser)
    assert item2.can_view(curator)
    assert item2.can_view(developer)
    assert item2.can_view(manager_A)
    assert item2.can_view(administrator_A)
    assert item2.can_view(collection_user_A)
    assert item2.can_view(restricted_user_A)
    assert not item2.can_view(external_user_A)
    assert not item2.can_view(manager_B)
    assert not item2.can_view(administrator_B)
    assert not item2.can_view(collection_user_B)
    assert not item2.can_view(restricted_user_B)
    assert not item2.can_view(external_user_A)

    # Item with unrestrictive licence
    item3 = collection_item_factory(
        collection=closed_collection_A,
        created_by=collection_user_A,
        licence=unrestrictive_licence,
    )

    assert item3.can_view(superuser)
    assert item3.can_view(curator)
    assert item3.can_view(developer)
    assert item3.can_view(manager_A)
    assert item3.can_view(administrator_A)
    assert item3.can_view(collection_user_A)
    assert item3.can_view(restricted_user_A)
    assert item3.can_view(external_user_A)
    assert item3.can_view(manager_B)
    assert item3.can_view(administrator_B)
    assert item3.can_view(collection_user_B)
    assert item3.can_view(restricted_user_B)

    # Item with inactive licence
    item4 = collection_item_factory(
        collection=closed_collection_A,
        created_by=collection_user_A,
        licence=inactive_restrictive_licence,
    )

    assert item4.can_view(superuser)
    assert item4.can_view(curator)
    assert item4.can_view(developer)
    assert item4.can_view(manager_A)
    assert item4.can_view(administrator_A)
    assert item4.can_view(collection_user_A)
    assert item4.can_view(restricted_user_A)
    assert item4.can_view(external_user_A)
    assert item4.can_view(manager_B)
    assert item4.can_view(administrator_B)
    assert item4.can_view(collection_user_B)
    assert item4.can_view(restricted_user_B)


@pytest.mark.django_db
def test_objects_manager(
    collection_item_factory,
    superuser,
    developer,
    curator,
    manager_A,
    manager_B,
    administrator_A,
    administrator_B,
    closed_collection_A,
    closed_collection_B,
    collection_user_A,
    collection_user_B,
    restricted_user_A,
    restricted_user_B,
    external_user_A,
    restrictive_licence,
    inactive_restrictive_licence,
    unrestrictive_licence,
):
    assert CollectionItem.objects.count() == 0

    item1 = collection_item_factory(
        collection=closed_collection_A,
        created_by=collection_user_A,
        licence=restrictive_licence,
    )

    item2 = collection_item_factory(
        collection=closed_collection_A,
        created_by=collection_user_A,
        licence=unrestrictive_licence,
    )

    item3 = collection_item_factory(
        collection=closed_collection_A,
        created_by=collection_user_A,
        licence=inactive_restrictive_licence,
    )

    item4 = collection_item_factory(
        collection=closed_collection_A,
        created_by=restricted_user_A,
        licence=restrictive_licence,
    )

    item5 = collection_item_factory(
        collection=closed_collection_A,
        created_by=restricted_user_A,
        licence=unrestrictive_licence,
    )

    item6 = collection_item_factory(
        collection=closed_collection_A,
        created_by=restricted_user_A,
        licence=inactive_restrictive_licence,
    )

    item7 = collection_item_factory(
        collection=closed_collection_B,
        created_by=collection_user_B,
        licence=restrictive_licence,
    )

    item8 = collection_item_factory(
        collection=closed_collection_B,
        created_by=collection_user_B,
        licence=unrestrictive_licence,
    )

    item9 = collection_item_factory(
        collection=closed_collection_B,
        created_by=collection_user_B,
        licence=inactive_restrictive_licence,
    )

    # Open Items
    assert CollectionItem.objects.open().count() == 6

    # Managed Items
    assert closed_collection_A.collection_type.is_admin(manager_A)
    assert closed_collection_B.collection_type.is_admin(manager_B)
    assert CollectionItem.objects.managed(superuser).count() == 0
    assert CollectionItem.objects.managed(curator).count() == 0
    assert CollectionItem.objects.managed(developer).count() == 0
    assert CollectionItem.objects.managed(manager_A).count() == 6
    assert CollectionItem.objects.managed(manager_B).count() == 3
    assert CollectionItem.objects.managed(administrator_A).count() == 0
    assert CollectionItem.objects.managed(administrator_B).count() == 0
    assert CollectionItem.objects.managed(collection_user_A).count() == 0
    assert CollectionItem.objects.managed(collection_user_B).count() == 0
    assert CollectionItem.objects.managed(restricted_user_A).count() == 0
    assert CollectionItem.objects.managed(restricted_user_B).count() == 0
    assert CollectionItem.objects.managed(external_user_A).count() == 0

    # Administered Items
    assert closed_collection_A.is_admin(administrator_A)
    assert closed_collection_B.is_admin(administrator_B)
    assert CollectionItem.objects.administered(superuser).count() == 0
    assert CollectionItem.objects.administered(curator).count() == 0
    assert CollectionItem.objects.administered(developer).count() == 0
    assert CollectionItem.objects.administered(manager_A).count() == 0
    assert CollectionItem.objects.administered(manager_B).count() == 0
    assert CollectionItem.objects.administered(administrator_A).count() == 6
    assert CollectionItem.objects.administered(administrator_B).count() == 3
    assert CollectionItem.objects.administered(collection_user_A).count() == 0
    assert CollectionItem.objects.administered(collection_user_B).count() == 0
    assert CollectionItem.objects.administered(restricted_user_A).count() == 0
    assert CollectionItem.objects.administered(restricted_user_B).count() == 0
    assert CollectionItem.objects.administered(external_user_A).count() == 0

    # Shared Items
    assert CollectionItem.objects.shared(superuser).count() == 0
    assert CollectionItem.objects.shared(curator).count() == 0
    assert CollectionItem.objects.shared(developer).count() == 0
    assert CollectionItem.objects.shared(manager_A).count() == 0
    assert CollectionItem.objects.shared(manager_B).count() == 0
    assert CollectionItem.objects.shared(administrator_A).count() == 0
    assert CollectionItem.objects.shared(administrator_B).count() == 0
    assert CollectionItem.objects.shared(collection_user_A).count() == 6
    assert CollectionItem.objects.shared(collection_user_B).count() == 3
    assert CollectionItem.objects.shared(restricted_user_A).count() == 0
    assert CollectionItem.objects.shared(restricted_user_B).count() == 0
    assert CollectionItem.objects.shared(external_user_A).count() == 0

    # User Items
    assert CollectionItem.objects.user(superuser).count() == 0
    assert CollectionItem.objects.user(curator).count() == 0
    assert CollectionItem.objects.user(developer).count() == 0
    assert CollectionItem.objects.user(manager_A).count() == 0
    assert CollectionItem.objects.user(manager_B).count() == 0
    assert CollectionItem.objects.user(administrator_A).count() == 0
    assert CollectionItem.objects.user(administrator_B).count() == 0
    assert CollectionItem.objects.user(collection_user_A).count() == 3
    assert CollectionItem.objects.user(collection_user_B).count() == 3
    assert CollectionItem.objects.user(restricted_user_A).count() == 3
    assert CollectionItem.objects.user(restricted_user_B).count() == 0
    assert CollectionItem.objects.user(external_user_A).count() == 0

    # Viewable Items
    assert CollectionItem.objects.can_view(superuser).count() == 9
    assert CollectionItem.objects.can_view(curator).count() == 9
    assert CollectionItem.objects.can_view(developer).count() == 9
    assert CollectionItem.objects.can_view(manager_A).count() == 8
    assert CollectionItem.objects.can_view(manager_B).count() == 7
    assert CollectionItem.objects.can_view(administrator_A).count() == 8
    assert CollectionItem.objects.can_view(administrator_B).count() == 7
    assert CollectionItem.objects.can_view(collection_user_A).count() == 8
    assert CollectionItem.objects.can_view(collection_user_B).count() == 7
    assert CollectionItem.objects.can_view(restricted_user_A).count() == 7
    assert CollectionItem.objects.can_view(restricted_user_B).count() == 6
    assert CollectionItem.objects.can_view(external_user_A).count() == 6


@pytest.mark.django_db
def test_can_change(
    collection_item_factory,
    superuser,
    developer,
    curator,
    manager_A,
    manager_B,
    administrator_A,
    administrator_B,
    closed_collection_A,
    closed_collection_B,
    collection_user_A,
    collection_user_B,
    restricted_user_A,
    restricted_user_B,
    external_user_A,
    restrictive_licence,
):
    item1 = collection_item_factory(
        collection=closed_collection_A,
        created_by=collection_user_A,
        licence=restrictive_licence,
    )

    assert item1.can_change(superuser)
    assert not item1.can_change(developer)
    assert item1.can_change(curator)
    assert item1.can_change(manager_A)
    assert not item1.can_change(manager_B)
    assert item1.can_change(administrator_A)
    assert not item1.can_change(administrator_B)
    assert item1.can_change(collection_user_A)
    assert not item1.can_change(collection_user_B)
    assert not item1.can_change(restricted_user_A)
    assert not item1.can_change(restricted_user_B)
    assert not item1.can_change(external_user_A)

    item2 = collection_item_factory(
        collection=closed_collection_A,
        created_by=restricted_user_A,
        licence=restrictive_licence,
    )

    assert item2.can_change(superuser)
    assert not item2.can_change(developer)
    assert item2.can_change(curator)
    assert item2.can_change(manager_A)
    assert not item2.can_change(manager_B)
    assert item2.can_change(administrator_A)
    assert not item2.can_change(administrator_B)
    assert item2.can_change(collection_user_A)
    assert not item2.can_change(collection_user_B)
    assert item2.can_change(restricted_user_A)
    assert not item2.can_change(restricted_user_B)
    assert not item2.can_change(external_user_A)


@pytest.mark.django_db
def test_can_delete(
    collection_item_factory,
    superuser,
    developer,
    curator,
    manager_A,
    manager_B,
    administrator_A,
    administrator_B,
    closed_collection_A,
    closed_collection_B,
    collection_user_A,
    collection_user_B,
    restricted_user_A,
    restricted_user_B,
    external_user_A,
    restrictive_licence,
):
    item1 = collection_item_factory(
        collection=closed_collection_A,
        created_by=collection_user_A,
        licence=restrictive_licence,
    )

    assert item1.can_delete(superuser)
    assert not item1.can_delete(developer)
    assert not item1.can_delete(curator)
    assert item1.can_delete(manager_A)
    assert not item1.can_delete(manager_B)
    assert item1.can_delete(administrator_A)
    assert not item1.can_delete(administrator_B)
    assert item1.can_delete(collection_user_A)
    assert not item1.can_delete(collection_user_B)
    assert not item1.can_delete(restricted_user_A)
    assert not item1.can_delete(restricted_user_B)
    assert not item1.can_delete(external_user_A)

    item2 = collection_item_factory(
        collection=closed_collection_A,
        created_by=restricted_user_A,
        licence=restrictive_licence,
    )

    assert item2.can_delete(superuser)
    assert not item2.can_delete(developer)
    assert not item2.can_delete(curator)
    assert item2.can_delete(manager_A)
    assert not item2.can_delete(manager_B)
    assert item2.can_delete(administrator_A)
    assert not item2.can_delete(administrator_B)
    assert item2.can_delete(collection_user_A)
    assert not item2.can_delete(collection_user_B)
    assert item2.can_delete(restricted_user_A)
    assert not item2.can_delete(restricted_user_B)
    assert not item2.can_delete(external_user_A)
