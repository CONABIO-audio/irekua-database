from django_filters import rest_framework as filters

from irekua_annotations.models import EventType
from irekua_annotations.models import AnnotationType
from irekua_terms.models import TermType
from irekua_terms.models import Term
from irekua_items.models import ItemType
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
    term_types = filters.ModelChoiceFilter(
        queryset=TermType.objects.all(),
        widget=get_autocomplete_widget(model=TermType),
    )

    should_imply = filters.ModelChoiceFilter(
        queryset=Term.objects.all(), widget=get_autocomplete_widget(model=Term)
    )

    annotation_types = filters.ModelChoiceFilter(
        queryset=AnnotationType.objects.all(),
        widget=get_autocomplete_widget(model=AnnotationType),
    )

    item_types = filters.ModelChoiceFilter(
        queryset=ItemType.objects.all(), widget=get_autocomplete_widget(model=ItemType)
    )

    class Meta:
        model = EventType

        fields = {
            "name": ["exact", "icontains"],
            "restrict_annotation_types": ["exact"],
            "term_types__name": ["exact", "icontains"],
            "annotation_types__name": ["exact", "icontains"],
            "item_types__name": ["exact", "icontains"],
        }
