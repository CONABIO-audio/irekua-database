import pytest

from irekua_collections.models import Collection

# pylint: disable=unused-wildcard-import,wildcard-import
from irekua_database.tests.fixtures.users import *
from irekua_database.tests.fixtures.roles import *
from irekua_collections.tests.fixtures.collection_types import *


actions = [
    "add",
    "change",
    "delete",
    "view",
]


models = [
    "collectionitem",
    "collectiondevice",
    "collectionsite",
    "samplingevent",
    "deployment",
    "annotation",
]


@pytest.fixture
@pytest.mark.django_db
def permissive_role(role_factory):
    role = role_factory("permissive_role")

    for action in actions:
        for model in models:
            role.add_permission_from_codename(f"{action}_{model}")
    return role


@pytest.fixture
@pytest.mark.django_db
def collection_factory():
    def create_collection(
        name,
        collection_type,
        description=None,
        metadata=None,
        institutions=None,
        logo=None,
        administrators=None,
        is_open=False,
    ):
        if description is None:
            description = f"Collection {name}"

        if institutions is None:
            institutions = []

        if administrators is None:
            administrators = []

        collection = Collection.objects.create(
            name=name,
            collection_type=collection_type,
            description=description,
            metadata=metadata,
            logo=logo,
            is_open=is_open,
        )

        for institution in institutions:
            collection.institutions.add(institution)

        for administrator in administrators:
            collection.administrators.add(administrator)

        return collection

    return create_collection


@pytest.fixture
@pytest.mark.django_db
def closed_collection_A(
    collection_factory,
    collection_type_A,
    administrator_A,
    restricted_user_A,
    collection_user_A,
    restrictive_role,
    permissive_role,
):
    collection = collection_factory(
        name="closed_collection_A",
        collection_type=collection_type_A,
        administrators=[administrator_A],
        is_open=False,
    )

    collection.users.add(
        restricted_user_A,
        through_defaults={
            "role": restrictive_role,
        },
    )

    collection.users.add(
        collection_user_A,
        through_defaults={
            "role": permissive_role,
        },
    )

    return collection


@pytest.fixture
@pytest.mark.django_db
def closed_collection_B(
    collection_factory,
    collection_type_B,
    manager_B,
    administrator_B,
    restricted_user_B,
    collection_user_B,
    restrictive_role,
    permissive_role,
):
    collection = collection_factory(
        name="closed_collection_B",
        collection_type=collection_type_B,
        administrators=[administrator_B],
        is_open=False,
    )

    collection.users.add(
        restricted_user_B,
        through_defaults={
            "role": restrictive_role,
        },
    )

    collection.users.add(
        collection_user_B,
        through_defaults={
            "role": permissive_role,
        },
    )

    return collection


@pytest.fixture
@pytest.mark.django_db
def open_collection_A(
    collection_factory,
    collection_type_A,
):
    return collection_factory(
        name="open_collection_A",
        collection_type=collection_type_A,
        is_open=True,
    )
