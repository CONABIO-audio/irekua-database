from django_filters import rest_framework as filters

from irekua_devices.models import PhysicalDevice
from irekua_devices.models import Device
from irekua_devices.models import DeviceType
from irekua_devices.models import DeviceBrand
from irekua_database.filters import IrekuaUserFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "name",
    "device__model",
    "device__brand__name",
)


ordering_fields = (
    "created_on",
    "name",
)


class Filter(IrekuaUserFilter):
    device__device_type = filters.ModelChoiceFilter(
        queryset=DeviceType.objects.all(),
        widget=get_autocomplete_widget(model=DeviceType),
    )

    device__brand = filters.ModelChoiceFilter(
        queryset=DeviceBrand.objects.all(),
        widget=get_autocomplete_widget(model=DeviceBrand),
    )

    device = filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        widget=get_autocomplete_widget(model=Device),
    )

    class Meta:
        model = PhysicalDevice

        fields = {
            "name": ["exact", "icontains"],
            "device__brand__name": ["exact", "icontains"],
            "device__device_type__name": ["exact", "icontains"],
            "device__model": ["exact", "icontains"],
            "serial_number": ["exact", "icontains"],
        }
