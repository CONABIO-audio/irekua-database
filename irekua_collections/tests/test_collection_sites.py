import pytest

from irekua_collections.models import CollectionSite

from irekua_database.tests.fixtures.users import *
from irekua_collections.tests.fixtures.collection_sites import *
from irekua_collections.tests.fixtures.data_collections import *


@pytest.mark.django_db
def test_collection_site_A(collection_site_A):
    assert isinstance(collection_site_A, CollectionSite)


@pytest.mark.django_db
def test_clean_associated_users(
    closed_collection_A,
    collection_site_A,
    collection_user_A,
    collection_user_B,
):
    # Check that "collection_site_A" is a site registered in the collection
    # "closed_collection_A"
    assert collection_site_A.collection == closed_collection_A

    # Check that "collection_user_A" is indeed a user of the collection
    # "closed_collection_A"
    assert closed_collection_A.is_user(collection_user_A)

    # Check that "collection_user_B" is not a user of the collection
    # "closed_collection_A"
    assert not closed_collection_A.is_user(collection_user_B)

    collection_site_A.associated_users.add(collection_user_A)
    collection_site_A.clean_associated_users()

    with pytest.raises(Exception):
        collection_site_A.associated_users.add(collection_user_B)
        collection_site_A.clean_associated_users()
