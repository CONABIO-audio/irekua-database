import pytest
import random

from irekua_collections.models import CollectionItem

# pylint: disable=unused-wildcard-import,wildcard-import
from irekua_database.tests.fixtures.users import *
from irekua_items.tests.fixtures.item_types import *
from irekua_items.tests.fixtures.mime_types import *
from irekua_items.tests.fixtures.licences import *
from irekua_collections.tests.fixtures.data_collections import *


@pytest.fixture
@pytest.mark.django_db
def collection_item_factory(item_type_A, audio_wav):
    def create_collection_item(
        collection,
        created_by,
        captured_on=None,
        captured_on_day=None,
        captured_on_hour=None,
        captured_on_month=None,
        captured_on_second=None,
        captured_on_timezone=None,
        captured_on_year=None,
        collection_device=None,
        collection_metadata=None,
        collection_site=None,
        deployment=None,
        hash=None,
        item_file=None,
        item_type=None,
        licence=None,
        media_info=None,
        metadata=None,
        mime_type=None,
        sampling_event=None,
        source=None,
        source_foreign_key="",
        tags=None,
    ):
        if tags is None:
            tags = []

        if media_info is None:
            media_info = ""

        if item_type is None:
            item_type = item_type_A

        if mime_type is None:
            mime_type = audio_wav

        if hash is None:
            hash = str(random.getrandbits(128))

        item = CollectionItem.objects.create(
            captured_on=captured_on,
            captured_on_day=captured_on_day,
            captured_on_hour=captured_on_hour,
            captured_on_month=captured_on_month,
            captured_on_second=captured_on_second,
            captured_on_timezone=captured_on_timezone,
            captured_on_year=captured_on_year,
            collection=collection,
            collection_device=collection_device,
            collection_metadata=collection_metadata,
            collection_site=collection_site,
            created_by=created_by,
            deployment=deployment,
            hash=hash,
            item_file=item_file,
            item_type=item_type,
            licence=licence,
            media_info=media_info,
            metadata=metadata,
            mime_type=mime_type,
            sampling_event=sampling_event,
            source=source,
            source_foreign_key=source_foreign_key,
        )

        for tag in tags:
            item.tags.add(tag)

        return item

    return create_collection_item


@pytest.fixture
@pytest.mark.django_db
def collection_item_A1(
    collection_item_factory,
    item_type_A,
    audio_wav,
    closed_collection_A,
    collection_user_A,
    restrictive_licence,
):
    return collection_item_factory(
        collection=closed_collection_A,
        created_by=collection_user_A,
        item_type=item_type_A,
        mime_type=audio_wav,
        licence=restrictive_licence,
    )


@pytest.fixture
@pytest.mark.django_db
def collection_item_A2(
    collection_item_factory,
    item_type_A,
    audio_wav,
    closed_collection_A,
    collection_user_A,
    inactive_restrictive_licence,
):
    return collection_item_factory(
        collection=closed_collection_A,
        created_by=collection_user_A,
        item_type=item_type_A,
        mime_type=audio_wav,
        licence=inactive_restrictive_licence,
    )


@pytest.fixture
@pytest.mark.django_db
def collection_item_A3(
    collection_item_factory,
    item_type_A,
    audio_wav,
    closed_collection_A,
    collection_user_A,
    unrestrictive_licence,
):
    return collection_item_factory(
        collection=closed_collection_A,
        created_by=collection_user_A,
        item_type=item_type_A,
        mime_type=audio_wav,
        licence=unrestrictive_licence,
    )
