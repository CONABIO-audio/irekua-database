from irekua_geo.models import SiteType
from irekua_database.filters import IrekuaFilter


search_fields = (
    "name",
    "description",
)


ordering_fields = (
    "created_on",
    "name",
)


class Filter(IrekuaFilter):
    class Meta:
        model = SiteType

        fields = {
            "name": ["exact", "icontains"],
            "point_site": ["exact"],
            "linestring_site": ["exact"],
            "multilinestring_site": ["exact"],
            "multipoint_site": ["exact"],
            "multipolygon_site": ["exact"],
            "polygon_site": ["exact"],
        }
