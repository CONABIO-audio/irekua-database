from django_filters import rest_framework as filters

from irekua_collections.models import DeploymentType
from irekua_devices.models import DeviceType
from irekua_items.models import ItemType

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
    device_type = filters.ModelChoiceFilter(
        queryset=DeviceType.objects.all(),
        widget=get_autocomplete_widget(model=DeviceType),
    )

    item_types = filters.ModelChoiceFilter(
        queryset=ItemType.objects.all(), widget=get_autocomplete_widget(model=ItemType)
    )

    class Meta:
        model = DeploymentType

        fields = {
            "name": ["exact", "icontains"],
            "device_type__name": ["exact", "icontains"],
            "restrict_item_types": ["exact"],
            "item_types__name": ["exact", "icontains"],
        }
