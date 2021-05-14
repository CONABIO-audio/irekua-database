from django.utils.translation import gettext as _
from django_filters import rest_framework as filters

from irekua_collections.models import Collection
from irekua_collections.models import CollectionType
from irekua_collections.models import CollectionDevice
from irekua_devices.models import PhysicalDevice
from irekua_devices.models import Device
from irekua_devices.models import DeviceBrand
from irekua_devices.models import DeviceType
from irekua_database.filters import IrekuaUserFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "collection_name",
    "physical_device__device__brand__name",
    "physical_device__device__device_type__name",
)

ordering_fields = (
    "created_on",
    "collection_name",
)


class Filter(IrekuaUserFilter):
    collection = filters.ModelChoiceFilter(
        queryset=Collection.objects.all(),
        widget=get_autocomplete_widget(model=Collection),
        label=_("Collection"),
    )

    collection_type = filters.ModelChoiceFilter(
        queryset=CollectionType.objects.all(),
        field_name="collection__collection_type",
        widget=get_autocomplete_widget(model=CollectionType),
        label=_("Collection type"),
    )

    physical_device = filters.ModelChoiceFilter(
        queryset=PhysicalDevice.objects.all(),
        widget=get_autocomplete_widget(model=PhysicalDevice),
        label=_("Physical device"),
    )

    device = filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        field_name="physical_device__device",
        widget=get_autocomplete_widget(model=Device),
        label=_("Device"),
    )

    brand = filters.ModelChoiceFilter(
        queryset=DeviceBrand.objects.all(),
        field_name="physical_device__device__brand",
        widget=get_autocomplete_widget(model=DeviceBrand),
        label=_("Brand"),
    )

    device_type = filters.ModelChoiceFilter(
        queryset=DeviceType.objects.all(),
        field_name="physical_device__device__device_type",
        widget=get_autocomplete_widget(model=DeviceType),
        label=_("Device type"),
    )

    class Meta:
        model = CollectionDevice

        fields = {
            "collection_name": ["icontains"],
        }
