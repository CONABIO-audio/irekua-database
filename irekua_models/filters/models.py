from django_filters import rest_framework as filters

from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget
from irekua_models.models import Model
from irekua_terms.models import Term
from irekua_items.models import ItemType
from irekua_annotations.models import AnnotationType
from irekua_annotations.models import EventType


search_fields = (
    "name",
    "description",
)


ordering_fields = (
    "created_on",
    "name",
)


class Filter(IrekuaFilter):
    annotation_type = filters.ModelChoiceFilter(
        queryset=AnnotationType.objects.all(),
        widget=get_autocomplete_widget(model=AnnotationType),
    )

    item_types = filters.ModelMultipleChoiceFilter(
        queryset=ItemType.objects.all(),
        widget=get_autocomplete_widget(model=ItemType, multiple=True),
    )

    event_types = filters.ModelMultipleChoiceFilter(
        queryset=EventType.objects.all(),
        widget=get_autocomplete_widget(model=EventType, multiple=True),
    )

    terms = filters.ModelMultipleChoiceFilter(
        queryset=Term.objects.all(),
        widget=get_autocomplete_widget(model=Term, multiple=True),
    )

    class Meta:
        model = Model

        fields = {
            "name": ["exact", "icontains"],
            "repository": ["exact", "icontains"],
        }
