import pytest

from irekua_items.tests.fixtures.items import *
from irekua_items.tests.fixtures.media_info_types import *

from irekua_upload.models import MediaInfoExtractor


@pytest.fixture
@pytest.mark.django_db
def media_info_extractor_factory(generate_random_python_file, media_info_type_A):
    def create_media_info_extractor(
        name,
        mime_type,
        media_info_type=None,
        devices=None,
        item_types=None,
        device_types=None,
        python_file=None,
        javascript_file=None,
    ):
        if devices is None:
            devices = []

        if item_types is None:
            item_types = []

        if device_types is None:
            device_types = []

        if media_info_type is None:
            media_info_type = media_info_type_A

        if python_file is None:
            python_file = generate_random_python_file()

        media_info_extractor = MediaInfoExtractor.objects.create(
            name=name,
            mime_type=mime_type,
            media_info_type=media_info_type,
        )

        for item_type in item_types:
            media_info_extractor.item_types.add(item_type)

        for device in devices:
            media_info_extractor.devices.add(device)

        for device_type in device_types:
            media_info_extractor.device_types.add(device_type)

        return media_info_extractor

    return create_media_info_extractor
