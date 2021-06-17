import pytest
from irekua_collections.models import CollectionSite

from irekua_collections.tests.fixtures.collection_sites import *
from irekua_collections.tests.fixtures.data_collections import *
from irekua_geo.tests.fixtures.site import *
from irekua_geo.tests.fixtures.site_type import *


@pytest.fixture
@pytest.mark.django_db
def collection_site_factory():
    def create_collection_site(
        site,
        site_type,
        collection,
        metadata=None,
        collection_metadata=None,
        collection_name=None,
        site_descriptors=None,
        parent_site=None,
        associated_users=None,
    ):
        if associated_users is None:
            associated_users = []

        if site_descriptors is None:
            site_descriptors = []

        collection_site = CollectionSite.objects.create(
            site=site,
            site_type=site_type,
            collection=collection,
            metadata=metadata,
            collection_metadata=collection_metadata,
            parent_site=parent_site,
        )

        collection_site.site_descriptors.add(*site_descriptors)
        collection_site.associated_users.add(*associated_users)
        return collection_site

    return create_collection_site


@pytest.fixture
@pytest.mark.django_db
def collection_site_A(
    collection_site_factory,
    closed_collection_A,
    site_type_A,
    point_site_A,
):
    return collection_site_factory(
        point_site_A,
        site_type_A,
        closed_collection_A,
        collection_name="collection site A",
    )
