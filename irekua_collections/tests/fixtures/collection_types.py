import pytest

from irekua_collections.models import CollectionType

# pylint: disable=wildcard-import,unused-wildcard-import
from irekua_database.tests.fixtures import *


@pytest.fixture(scope="module")
@pytest.mark.django_db
def collection_type_factory():
    def create_collection_type(
        name,
        description=None,
        anyone_can_create=False,
        restrict_site_types=False,
        restrict_annotation_types=False,
        restrict_item_types=False,
        restrict_licence_types=False,
        restrict_device_types=False,
        restrict_event_types=False,
        restrict_sampling_event_types=False,
        restrict_deployment_types=False,
        administrators=None,
        roles=None,
    ):
        if administrators is None:
            administrators = []

        if roles is None:
            roles = []

        if description is None:
            description = f"Collections of type {name}"

        collection_type = CollectionType.objects.create(
            name=name,
            description=description,
            anyone_can_create=anyone_can_create,
            restrict_site_types=restrict_site_types,
            restrict_annotation_types=restrict_annotation_types,
            restrict_item_types=restrict_item_types,
            restrict_licence_types=restrict_licence_types,
            restrict_device_types=restrict_device_types,
            restrict_event_types=restrict_event_types,
            restrict_sampling_event_types=restrict_sampling_event_types,
            restrict_deployment_types=restrict_deployment_types,
        )

        for role in roles:
            collection_type.roles.add(role)

        for administrator in administrators:
            collection_type.administrators.add(administrator)

        return collection_type

    return create_collection_type


@pytest.fixture
@pytest.mark.django_db
def collection_type_A(manager_A, collection_type_factory):
    return collection_type_factory(
        "collection type A", administrators=[manager_A]
    )


@pytest.fixture
@pytest.mark.django_db
def collection_type_B(manager_B, collection_type_factory):
    return collection_type_factory(
        "collection type B", administrators=[manager_B]
    )
