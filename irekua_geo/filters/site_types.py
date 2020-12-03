from django_filters import rest_framework as filters

from irekua_geo.models import SiteType
from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "name",
    "description",
)


ordering_fields = (
    "created_on",
    "name",
)


class Filter(IrekuaFilter):
    subsite_types = filters.ModelChoiceFilter(
        queryset=SiteType.objects.all(),
        widget=get_autocomplete_widget(model=SiteType),
    )

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
            "can_have_subsites": ["exact"],
            "restrict_subsite_types": ["exact"],
        }
