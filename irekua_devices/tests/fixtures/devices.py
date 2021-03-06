import uuid
import pytest

# pytest: disable=wildcard-import,unused-wildcard-import
from irekua_items.tests.fixtures.item_types import *
from irekua_devices.tests.fixtures.device_types import *
from irekua_devices.tests.fixtures.device_brands import *

from irekua_devices.models import Device


@pytest.fixture
@pytest.mark.django_db
def device_factory(brand_A):
    def create_device(
        device_type,
        brand=None,
        model=None,
        configuration_schema=None,
    ):
        if brand is None:
            brand = brand_A

        if model is None:
            model = str(uuid.uuid1())

        return Device.objects.create(
            device_type=device_type,
            brand=brand,
            model=model,
            configuration_schema=configuration_schema,
        )

    return create_device


@pytest.fixture
@pytest.mark.django_db
def camera_A(device_factory, camera):
    return device_factory(camera, model="camera_A")


@pytest.fixture
@pytest.mark.django_db
def camera_B(device_factory, camera):
    return device_factory(camera, model="camera_B")


@pytest.fixture
@pytest.mark.django_db
def recorder_A(device_factory, recorder):
    return device_factory(recorder, model="recorder_A")


@pytest.fixture
@pytest.mark.django_db
def recorder_B(device_factory, recorder):
    return device_factory(recorder, model="recorder_B")
