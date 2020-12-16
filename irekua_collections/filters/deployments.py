from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from irekua_collections.models import Collection
from irekua_collections.models import CollectionType
from irekua_collections.models import CollectionDevice
from irekua_collections.models import SamplingEvent
from irekua_collections.models import Deployment
from irekua_collections.models import DeploymentType
from irekua_collections.models import SamplingEventType
from irekua_collections.models import CollectionSite
from irekua_devices.models import PhysicalDevice
from irekua_devices.models import Device
from irekua_devices.models import DeviceBrand
from irekua_devices.models import DeviceType
from irekua_geo.models import SiteType
from irekua_geo.models import Site
from irekua_database.filters import IrekuaUserFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "id",
    "deployment_type__name",
    "collection_device__collection_name",
    "sampling_event__collection_site__collection_name",
)

ordering_fields = (
    "created_on",
    "deployment_type__name",
    "collection_device__collection_name",
    "sampling_event__collection_site__collection_name",
)


class Filter(IrekuaUserFilter):
    deployment_type = filters.ModelChoiceFilter(
        queryset=DeploymentType.objects.all(),
        widget=get_autocomplete_widget(model=DeploymentType),
    )

    collection = filters.ModelChoiceFilter(
        queryset=Collection.objects.all(),
        field_name="sampling_event__collection",
        label=_("Collection"),
        widget=get_autocomplete_widget(model=Collection),
    )

    collection_type = filters.ModelChoiceFilter(
        queryset=CollectionType.objects.all(),
        label=_("Collection type"),
        field_name="sampling_event__collection__collection_type",
        widget=get_autocomplete_widget(model=CollectionType),
    )

    sampling_event = filters.ModelChoiceFilter(
        queryset=SamplingEvent.objects.all(),
        widget=get_autocomplete_widget(model=SamplingEvent),
    )

    sampling_event_type = filters.ModelChoiceFilter(
        queryset=SamplingEventType.objects.all(),
        field_name="sampling_event__sampling_event_type",
        label=_("Sampling event type"),
        widget=get_autocomplete_widget(model=SamplingEventType),
    )

    collection_site = filters.ModelChoiceFilter(
        queryset=CollectionSite.objects.all(),
        field_name="sampling_event__collection_site",
        label=_("Collection site"),
        widget=get_autocomplete_widget(model=CollectionSite),
    )

    site = filters.ModelChoiceFilter(
        queryset=Site.objects.all(),
        label=_("Site"),
        field_name="sampling_event__collection_site__site",
        widget=get_autocomplete_widget(model=Site),
    )

    site_type = filters.ModelChoiceFilter(
        queryset=SiteType.objects.all(),
        label=_("Site type"),
        field_name="sampling_event__collection_site__site_type",
        widget=get_autocomplete_widget(model=SiteType),
    )

    collection_device = filters.ModelChoiceFilter(
        queryset=CollectionDevice.objects.all(),
        widget=get_autocomplete_widget(model=CollectionDevice),
    )

    physical_device = filters.ModelChoiceFilter(
        queryset=PhysicalDevice.objects.all(),
        label=_("Physical device"),
        field_name="collection_device__physical_device",
        widget=get_autocomplete_widget(model=PhysicalDevice),
    )

    device = filters.ModelChoiceFilter(
        queryset=Device.objects.all(),
        label=_("Device"),
        field_name="collection_device__physical_device__device",
        widget=get_autocomplete_widget(model=Device),
    )

    brand = filters.ModelChoiceFilter(
        queryset=DeviceBrand.objects.all(),
        label=_("Brand"),
        field_name="collection_device__physical_device__device__brand",
        widget=get_autocomplete_widget(model=DeviceBrand),
    )

    device_type = filters.ModelChoiceFilter(
        queryset=DeviceType.objects.all(),
        label=_("Device type"),
        field_name="collection_device__physical_device__device__device_type",
        widget=get_autocomplete_widget(model=DeviceType),
    )

    class Meta:
        model = Deployment

        fields = {
            "deployed_on": ["exact", "lt", "gt", "lte", "gte"],
            "recovered_on": ["exact", "lt", "gt", "lte", "gte"],
            "latitude": ["exact", "lt", "gt", "lte", "gte"],
            "longitude": ["exact", "lt", "gt", "lte", "gte"],
            "altitude": ["exact", "lt", "gt", "lte", "gte"],
        }
