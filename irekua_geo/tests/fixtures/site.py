import pytest
import random

from django.contrib.gis.geos import Point

from irekua_geo.models import get_site_class
from irekua_geo.models import Site


@pytest.fixture
@pytest.mark.django_db
def site_factory():
    def create_site(
        name,
        geometry=None,
        localities=None,
        geometry_type=Site.POINT,
        **kwargs,
    ):

        if localities is None:
            localities = []

        site_class = get_site_class(geometry_type)
        site = site_class.objects.create(
            name=name,
            geometry_type=geometry_type,
            geometry=geometry,
            **kwargs,
        )

        site.localities.add(*localities)

        return site

    return create_site


@pytest.fixture
@pytest.mark.django_db
def point_site_A(site_factory):
    latitude = random.random()
    longitude = random.random()
    geometry = Point(longitude, latitude)
    return site_factory(
        "site_A",
        geometry=geometry,
        latitude=latitude,
        longitude=longitude,
    )
