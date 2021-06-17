import pytest

from irekua_geo.models import SiteType


@pytest.fixture
@pytest.mark.django_db
def site_type_factory():
    def create_site_type(
        name,
        description=None,
        icon=None,
        site_descriptor_types=None,
        point_site=True,
        linestring_site=True,
        polygon_site=True,
        multi_point_site=True,
        multi_linestring_site=True,
        multi_polygon_site=True,
        can_have_subsites=True,
        restrict_subsite_types=False,
        subsite_types=None,
    ):
        if description is None:
            description = f"Site type {name}"

        if subsite_types is None:
            subsite_types = []

        if site_descriptor_types is None:
            site_descriptor_types = []

        site_type = SiteType.objects.create(
            name=name,
            description=description,
            icon=icon,
            point_site=point_site,
            linestring_site=linestring_site,
            polygon_site=polygon_site,
            multipoint_site=multi_point_site,
            multilinestring_site=multi_linestring_site,
            multipolygon_site=multi_polygon_site,
            can_have_subsites=can_have_subsites,
            restrict_subsite_types=restrict_subsite_types,
        )

        site_type.site_descriptor_types.add(*site_descriptor_types)
        site_type.subsite_types.add(*subsite_types)

        return site_type

    return create_site_type


@pytest.fixture
@pytest.mark.django_db
def site_type_A(site_type_factory):
    return site_type_factory("site_type_A")
