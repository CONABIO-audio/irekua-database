from django_filters import rest_framework as filters

from irekua_database.models import User
from irekua_database.models import Role
from irekua_geo.models import SiteType
from irekua_items.models import LicenceType
from irekua_items.models import ItemType
from irekua_devices.models import DeviceType
from irekua_annotations.models import AnnotationType
from irekua_annotations.models import EventType
from irekua_collections.models import CollectionType
from irekua_collections.models import DeploymentType
from irekua_collections.models import SamplingEventType

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
    administrators = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=get_autocomplete_widget(model=User),
    )

    site_types = filters.ModelChoiceFilter(
        queryset=SiteType.objects.all(),
        widget=get_autocomplete_widget(model=SiteType),
    )

    annotation_types = filters.ModelChoiceFilter(
        queryset=AnnotationType.objects.all(),
        widget=get_autocomplete_widget(model=AnnotationType),
    )

    licence_types = filters.ModelChoiceFilter(
        queryset=LicenceType.objects.all(),
        widget=get_autocomplete_widget(model=LicenceType),
    )

    event_types = filters.ModelChoiceFilter(
        queryset=EventType.objects.all(),
        widget=get_autocomplete_widget(model=EventType),
    )

    sampling_event_types = filters.ModelChoiceFilter(
        queryset=SamplingEventType.objects.all(),
        widget=get_autocomplete_widget(model=SamplingEventType),
    )

    item_types = filters.ModelChoiceFilter(
        queryset=ItemType.objects.all(),
        widget=get_autocomplete_widget(model=ItemType),
    )

    device_types = filters.ModelChoiceFilter(
        queryset=DeviceType.objects.all(),
        widget=get_autocomplete_widget(model=DeviceType),
    )

    deployment_types = filters.ModelChoiceFilter(
        queryset=DeploymentType.objects.all(),
        widget=get_autocomplete_widget(model=DeploymentType),
    )

    roles = filters.ModelChoiceFilter(
        queryset=Role.objects.all(),
        widget=get_autocomplete_widget(model=Role),
    )

    class Meta:
        model = CollectionType

        fields = {
            "name": ["exact", "icontains"],
            "anyone_can_create": ["exact"],
            "restrict_site_types": ["exact"],
            "restrict_annotation_types": ["exact"],
            "restrict_item_types": ["exact"],
            "restrict_licence_types": ["exact"],
            "restrict_device_types": ["exact"],
            "restrict_event_types": ["exact"],
            "restrict_sampling_event_types": ["exact"],
            "restrict_deployment_types": ["exact"],
        }
