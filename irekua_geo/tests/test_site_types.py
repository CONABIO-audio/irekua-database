from irekua_geo.tests.fixtures.site_type import *

from irekua_geo.models import SiteType


@pytest.mark.django_db
def test_site_type_A(site_type_A):
    assert isinstance(site_type_A, SiteType)
    assert site_type_A.name == "site_type_A"
