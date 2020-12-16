from django_filters import rest_framework as filters

from irekua_collections.models import CollectionItem
from irekua_collections.models import Collection
from irekua_collections.models import CollectionType
from irekua_collections.models import CollectionDevice
from irekua_collections.models import SamplingEvent
from irekua_collections.models import SamplingEventType
from irekua_collections.models import Deployment
from irekua_collections.models import DeploymentType
from irekua_collections.models import CollectionSite
from irekua_geo.models import Site
from irekua_geo.models import SiteType
from irekua_devices.models import PhysicalDevice
from irekua_devices.models import Device
from irekua_devices.models import DeviceBrand
from irekua_devices.models import DeviceType
from irekua_items.filters import items
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = items.search_fields


ordering_fields = items.ordering_fields


class Filter(items.Filter):
    collection = filters.ModelChoiceFilter(
        queryset=Collection.objects.all(),
        widget=get_autocomplete_widget(model=Collection),
    )

    collection_type = filters.ModelChoiceFilter(
        queryset=CollectionType.objects.all(),
        field_name="collection__collection_type",
        widget=get_autocomplete_widget(model=CollectionType),
    )

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

    sampling_event = filters.ModelChoiceFilter(
        queryset=SamplingEvent.objects.all(),
        widget=get_autocomplete_widget(model=SamplingEvent),
    )

    sampling_event_type = filters.ModelChoiceFilter(
        queryset=SamplingEventType.objects.all(),
        field_name="sampling_event__sampling_event_type",
        widget=get_autocomplete_widget(model=SamplingEventType),
    )

    deployment = filters.ModelChoiceFilter(
        queryset=Deployment.objects.all(),
        widget=get_autocomplete_widget(model=Deployment),
    )

    deployment_type = filters.ModelChoiceFilter(
        queryset=DeploymentType.objects.all(),
        field_name="deployment__deployment_type",
        widget=get_autocomplete_widget(model=DeploymentType),
    )

    collection_site = filters.ModelChoiceFilter(
        queryset=CollectionSite.objects.all(),
        widget=get_autocomplete_widget(model=CollectionSite),
    )

    site = filters.ModelChoiceFilter(
        queryset=Site.objects.all(),
        field_name="collection_site__site",
        widget=get_autocomplete_widget(model=Site),
    )

    site_type = filters.ModelChoiceFilter(
        queryset=SiteType.objects.all(),
        field_name="collection_site__site_type",
        widget=get_autocomplete_widget(model=SiteType),
    )

    class Meta(items.Filter.Meta):
        model = CollectionItem
