from django_filters import rest_framework as filters

from irekua_collections.models import CollectionAnnotation
from irekua_collections.models import Collection
from irekua_collections.models import CollectionType
from irekua_annotations.filters import user_annotations
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = user_annotations.search_fields


ordering_fields = user_annotations.ordering_fields


class Filter(user_annotations.Filter):
    collection = filters.ModelChoiceFilter(
        queryset=Collection.objects.all(),
        widget=get_autocomplete_widget(model=Collection),
    )

    collection_type = filters.ModelChoiceFilter(
        queryset=CollectionType.objects.all(),
        field_name="collection__collection_type",
        widget=get_autocomplete_widget(model=CollectionType),
    )

    class Meta(user_annotations.Filter.Meta):
        model = CollectionAnnotation
