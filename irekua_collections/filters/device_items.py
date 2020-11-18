from django_filters import rest_framework as filters

from irekua_collections.models import DeviceItem
from irekua_collections.models import CollectionDevice
from irekua_devices.models import PhysicalDevice
from irekua_devices.models import Device
from irekua_devices.models import DeviceBrand
from irekua_devices.models import DeviceType
from irekua_database.autocomplete import get_autocomplete_widget

from .collection_items import search_fields
from .collection_items import ordering_fields
from .collection_items import Filter as CollectionItemFilter


__all__ = [
    "search_fields",
    "ordering_fields",
    "Filter",
]


class Filter(CollectionItemFilter):
    collection_device = filters.ModelChoiceFilter(
        queryset=CollectionDevice.objects.all(),
        widget=get_autocomplete_widget(model=CollectionDevice),
    )

    physical_device = filters.ModelChoiceFilter(
        queryset=PhysicalDevice.objects.all(),
        field_name="collection_device__physical_device",
        widget=get_autocomplete_widget(model=PhysicalDevice),
    )

    device = filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        field_name="collection_device__physical_device__device",
        widget=get_autocomplete_widget(model=Device),
    )

    brand = filters.ModelChoiceFilter(
        queryset=DeviceBrand.objects.all(),
        field_name="collection_device__physical_device__device__brand",
        widget=get_autocomplete_widget(model=DeviceBrand),
    )

    device_type = filters.ModelChoiceFilter(
        queryset=DeviceType.objects.all(),
        field_name="collection_device__physical_device__device__device_type",
        widget=get_autocomplete_widget(model=DeviceType),
    )

    class Meta(CollectionItemFilter.Meta):
        model = DeviceItem

        fields = {
            **CollectionItemFilter.Meta.fields,
            "collection_device__physical_device__serial_number": ["exact", "icontains"],
        }
