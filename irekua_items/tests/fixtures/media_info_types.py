import pytest

from irekua_schemas.tests.fixtures.schemas import *
from irekua_items.models import MediaInfoType


@pytest.fixture
@pytest.mark.django_db
def media_info_type_factory(trivial_schema):
    def create_media_info_type(
        name,
        description=None,
        media_info_schema=None,
    ):
        if description is None:
            description = f"Media info {name}"

        if media_info_schema is None:
            media_info_schema = trivial_schema

        return MediaInfoType.objects.create(
            name=name,
            description=description,
            media_info_schema=media_info_schema,
        )

    return create_media_info_type


@pytest.fixture
@pytest.mark.django_db
def media_info_type_A(media_info_type_factory):
    return media_info_type_factory("media info type A")


@pytest.fixture
@pytest.mark.django_db
def media_info_type_B(media_info_type_factory):
    return media_info_type_factory("media info type B")


@pytest.fixture
@pytest.mark.django_db
def media_info_type_string(media_info_type_factory, string_schema):
    return media_info_type_factory(
        "media info type string",
        media_info_schema=string_schema,
    )


@pytest.fixture
@pytest.mark.django_db
def media_info_type_boolean(media_info_type_factory, boolean_schema):
    return media_info_type_factory(
        "media info type string",
        media_info_schema=boolean_schema,
    )
