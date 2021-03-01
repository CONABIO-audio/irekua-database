import pytest

from irekua_items.models import LicenceType
from irekua_items.models import Licence

# pytest: disable=wildcard-import,unused-wildcard-import
from irekua_database.tests.fixtures.users import *


@pytest.fixture
@pytest.mark.django_db
def licence_type_factory():
    def create_licence_type(
        name,
        description=None,
        icon=None,
        document_template=None,
        years_valid_for=99,
        can_view=False,
        can_download=False,
        can_view_annotations=False,
        can_annotate=False,
        can_vote_annotations=False,
    ):
        if description is None:
            description = f"Licence type {name}"

        return LicenceType.objects.create(
            name=name,
            description=description,
            icon=icon,
            document_template=document_template,
            years_valid_for=years_valid_for,
            can_view=can_view,
            can_download=can_download,
            can_view_annotations=can_view_annotations,
            can_annotate=can_annotate,
            can_vote_annotations=can_vote_annotations,
        )

    return create_licence_type


@pytest.fixture
@pytest.mark.django_db
def licence_factory():
    def create_licence(
        licence_type,
        created_by,
        document=None,
        metadata=None,
        is_active=True,
    ):
        return Licence.objects.create(
            licence_type=licence_type,
            created_by=created_by,
            document=document,
            metadata=metadata,
            is_active=is_active,
        )

    return create_licence


@pytest.fixture
@pytest.mark.django_db
def restrictive_long_licence_type(licence_type_factory):
    return licence_type_factory("restrictive_long_licence")


@pytest.fixture
@pytest.mark.django_db
def restrictive_short_licence_type(licence_type_factory):
    return licence_type_factory("restrictive_short_licence", years_valid_for=3)


@pytest.fixture
@pytest.mark.django_db
def unrestrictive_licence_type(licence_type_factory):
    return licence_type_factory(
        "unrestrictive_licence",
        can_download=True,
        can_vote_annotations=True,
        can_annotate=True,
        can_view=True,
        can_view_annotations=True,
    )


@pytest.fixture
@pytest.mark.django_db
def restrictive_licence(
    licence_factory,
    restrictive_long_licence_type,
    administrator_A,
):
    return licence_factory(restrictive_long_licence_type, administrator_A)


@pytest.fixture
@pytest.mark.django_db
def inactive_restrictive_licence(
    licence_factory,
    restrictive_long_licence_type,
    administrator_A,
):
    return licence_factory(
        restrictive_long_licence_type,
        administrator_A,
        is_active=False,
    )


@pytest.fixture
@pytest.mark.django_db
def unrestrictive_licence(
    licence_factory,
    unrestrictive_licence_type,
    administrator_A,
):
    return licence_factory(
        unrestrictive_licence_type,
        administrator_A,
    )
