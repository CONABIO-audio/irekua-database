from django_filters import rest_framework as filters

from irekua_geo.models import Site
from irekua_geo.models import Locality
from irekua_database.filters import IrekuaUserFilter

from irekua_database.autocomplete import get_autocomplete_widget


search_fields = ("name", "locality__name")


ordering_fields = (
    "created_on",
    "name",
)


class Filter(IrekuaUserFilter):
    locality = filters.ModelChoiceFilter(
        queryset=Locality.objects.all(),
        widget=get_autocomplete_widget(model=Locality),
    )

    class Meta:
        model = Site

        fields = {
            "name": ["exact", "icontains"],
            "geometry_type": ["exact"],
            "locality__name": ["exact", "icontains"],
        }
