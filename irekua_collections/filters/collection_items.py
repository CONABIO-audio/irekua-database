from django_filters import rest_framework as filters

from irekua_collections.models import CollectionItem
from irekua_collections.models import Collection
from irekua_collections.models import CollectionType
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

    class Meta(items.Filter.Meta):
        model = CollectionItem
