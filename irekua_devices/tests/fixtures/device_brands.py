import pytest

from irekua_devices.models import DeviceBrand


@pytest.fixture
@pytest.mark.django_db
def device_brand_factory():
    def create_device_brand(name, website=None, logo=None):
        return DeviceBrand.objects.create(
            name=name,
            website=website,
            logo=logo,
        )

    return create_device_brand


@pytest.fixture
@pytest.mark.django_db
def brand_A(device_brand_factory):
    return device_brand_factory("brand A")


@pytest.fixture
@pytest.mark.django_db
def brand_B(device_brand_factory):
    return device_brand_factory("brand B")
