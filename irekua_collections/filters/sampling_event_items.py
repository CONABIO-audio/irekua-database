from django_filters import rest_framework as filters

from irekua_collections.models import SamplingEventItem
from irekua_collections.models import SamplingEvent
from irekua_collections.models import SamplingEventType
from irekua_database.autocomplete import get_autocomplete_widget

from .site_items import search_fields
from .site_items import ordering_fields
from .site_items import Filter as SiteItemFilter


__all__ = [
    "search_fields",
    "ordering_fields",
    "Filter",
]


class Filter(SiteItemFilter):
    sampling_event = filters.ModelChoiceFilter(
        queryset=SamplingEvent.objects.all(),
        widget=get_autocomplete_widget(model=SamplingEvent),
    )

    sampling_event_type = filters.ModelChoiceFilter(
        queryset=SamplingEventType.objects.all(),
        field_name="sampling_event__sampling_event_type",
        widget=get_autocomplete_widget(model=SamplingEventType),
    )

    class Meta(SiteItemFilter.Meta):
        model = SamplingEventItem
