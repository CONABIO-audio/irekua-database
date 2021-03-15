import pytest

from irekua_items.models import ItemType

# pytest: disable=unused-wildcard-import,wildcard-import
from irekua_items.tests.fixtures.mime_types import *


@pytest.fixture
@pytest.mark.django_db
def item_type_factory():
    def create_item_type(
        name, description=None, mime_types=None, media_info_type=None
    ):
        if description is None:
            description = f"Item type {name}"

        if mime_types is None:
            mime_types = []

        item_type = ItemType.objects.create(
            name=name, description=description, media_info_type=media_info_type
        )

        for mime_type in mime_types:
            item_type.mime_types.add(mime_type)

        return item_type

    return create_item_type


@pytest.fixture
@pytest.mark.django_db
def item_type_A(item_type_factory, audio_wav):
    return item_type_factory("item_type_A", mime_types=[audio_wav])


@pytest.fixture
@pytest.mark.django_db
def item_type_B(item_type_factory):
    return item_type_factory("item_type_B")
