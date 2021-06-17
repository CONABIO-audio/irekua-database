from irekua_geo.tests.fixtures.site import *


@pytest.mark.django_db
def test_point_A(point_site_A):
    assert point_site_A.geometry.x == point_site_A.longitude
    assert point_site_A.geometry.y == point_site_A.latitude
