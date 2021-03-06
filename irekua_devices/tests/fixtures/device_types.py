import pytest

from irekua_devices.models import DeviceType

from irekua_items.tests.fixtures.item_types import *
from irekua_items.tests.fixtures.mime_types import *


@pytest.fixture
@pytest.mark.django_db
def device_type_factory():
    def create_device_type(name, description=None, mime_types=None):
        if description is None:
            description = f"Device type {name}"

        if mime_types is None:
            mime_types = []

        device_type = DeviceType.objects.create(
            name=name,
            description=description,
        )

        for mime_type in mime_types:
            device_type.mime_types.add(mime_type)

        return device_type

    return create_device_type


@pytest.fixture
@pytest.mark.django_db
def camera(device_type_factory, image_png, image_jpeg, video_avi):
    return device_type_factory("camara", mime_types=[image_png, image_jpeg, video_avi])


@pytest.fixture
@pytest.mark.django_db
def recorder(device_type_factory, audio_wav):
    return device_type_factory("recorder", mime_types=[audio_wav])
