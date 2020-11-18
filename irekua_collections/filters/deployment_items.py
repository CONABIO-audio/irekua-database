from django_filters import rest_framework as filters

from irekua_collections.models import DeploymentItem
from irekua_collections.models import Deployment
from irekua_collections.models import DeploymentType
from irekua_database.autocomplete import get_autocomplete_widget

from .sampling_event_items import search_fields
from .sampling_event_items import ordering_fields
from .sampling_event_items import Filter as SamplingEventItemFilter
from .device_items import Filter as DeviceItemFilter


__all__ = [
    "search_fields",
    "ordering_fields",
    "Filter",
]


class Filter(SamplingEventItemFilter, DeviceItemFilter):
    deployment = filters.ModelChoiceFilter(
        queryset=Deployment.objects.all(),
        widget=get_autocomplete_widget(model=Deployment),
    )

    deployment_type = filters.ModelChoiceFilter(
        queryset=DeploymentType.objects.all(),
        field_name="deployment__deployment_type",
        widget=get_autocomplete_widget(model=DeploymentType),
    )

    class Meta(SamplingEventItemFilter.Meta):
        model = DeploymentItem

        fields = {
            **SamplingEventItemFilter.Meta.fields,
            **DeviceItemFilter.Meta.fields,
        }
