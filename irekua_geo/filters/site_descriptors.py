from django_filters import rest_framework as filters

from irekua_geo.models import SiteDescriptor
from irekua_geo.models import SiteDescriptorType
from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "value",
    "descriptor_type__name",
)


ordering_fields = (
    "created_on",
    "value",
)


class Filter(IrekuaFilter):
    descriptor_type = filters.ModelChoiceFilter(
        queryset=SiteDescriptorType.objects.all(),
        widget=get_autocomplete_widget(model=SiteDescriptorType),
    )

    class Meta:
        model = SiteDescriptor

        fields = {
            "value": ["exact", "icontains"],
        }
