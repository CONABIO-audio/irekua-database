from django_filters import rest_framework as filters

from irekua_database.autocomplete import get_autocomplete_widget
from irekua_items.filters import licences
from irekua_collections.models import CollectionLicence
from irekua_collections.models import Collection
from irekua_collections.models import CollectionType


search_fields = licences.search_fields


ordering_fields = licences.ordering_fields


class Filter(licences.Filter):
    collection = filters.ModelChoiceFilter(
        queryset=Collection.objects.all(),
        widget=get_autocomplete_widget(model=Collection),
    )

    collection_type = filters.ModelChoiceFilter(
        queryset=CollectionType.objects.all(),
        field_name="collection__collection_type",
        widget=get_autocomplete_widget(model=CollectionType),
    )

    class Meta(licences.Filter.Meta):
        model = CollectionLicence
