from django_filters import rest_framework as filters

from irekua_collections.models import Collection
from irekua_collections.models import CollectionType
from irekua_collections.models import SamplingEvent
from irekua_collections.models import SamplingEventType
from irekua_collections.models import CollectionSite
from irekua_geo.models import SiteType
from irekua_geo.models import Site
from irekua_database.filters import IrekuaUserFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = ("id", "collection_site__collection_name", "sampling_event_type__name")


ordering_fields = (
    "created_on",
    "collection_site__collection_name",
    "sampling_event_type__name",
)


class Filter(IrekuaUserFilter):
    collection = filters.ModelChoiceFilter(
        queryset=Collection.objects.all(),
        widget=get_autocomplete_widget(model=Collection),
    )

    collection_type = filters.ModelChoiceFilter(
        queryset=CollectionType.objects.all(),
        field_name="collection__collection_type",
        widget=get_autocomplete_widget(model=CollectionType),
    )

    sampling_event_type = filters.ModelChoiceFilter(
        queryset=SamplingEventType.objects.all(),
        widget=get_autocomplete_widget(model=SamplingEventType),
    )

    collection_site = filters.ModelChoiceFilter(
        queryset=CollectionSite.objects.all(),
        widget=get_autocomplete_widget(model=CollectionSite),
    )

    site_type = filters.ModelChoiceFilter(
        queryset=SiteType.objects.all(),
        field_name="collection_site__site_type",
        widget=get_autocomplete_widget(model=SiteType),
    )

    site = filters.ModelChoiceFilter(
        queryset=Site.objects.all(),
        field_name="collection_site__site",
        widget=get_autocomplete_widget(model=Site),
    )

    class Meta:
        model = SamplingEvent

        fields = {
            "started_on": ["exact", "lt", "gt", "lte", "gte"],
            "ended_on": ["exact", "lt", "gt", "lte", "gte"],
        }
