from django_filters import rest_framework as filters

from irekua_devices.models import Device
from irekua_devices.models import DeviceType
from irekua_devices.models import DeviceBrand
from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "model",
    "brand__name",
    "device_type__name",
)


ordering_fields = (
    "created_on",
    "model",
)


class Filter(IrekuaFilter):
    device_type = filters.ModelChoiceFilter(
        queryset=DeviceType.objects.all(),
        widget=get_autocomplete_widget(model=DeviceType),
    )

    brand = filters.ModelChoiceFilter(
        queryset=DeviceBrand.objects.all(),
        widget=get_autocomplete_widget(model=DeviceBrand),
    )

    class Meta:
        model = Device

        fields = {
            "model": ["exact", "icontains"],
        }
