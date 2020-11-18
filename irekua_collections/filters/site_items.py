from django_filters import rest_framework as filters

from irekua_collections.models import SiteItem
from irekua_collections.models import CollectionSite
from irekua_geo.models import Site
from irekua_geo.models import SiteType
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

    class Meta(CollectionItemFilter.Meta):
        model = SiteItem
