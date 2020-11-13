from django_filters import rest_framework as filters

from irekua_annotations.models import Annotation
from irekua_annotations.models import AnnotationType
from irekua_annotations.models import EventType
from irekua_terms.models import TermType
from irekua_terms.models import Term
from irekua_items.models import ItemType
from irekua_items.models import Item
from irekua_database.filters import IrekuaUserFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "id",
    "labels__value",
    "labels__term_type__name",
    "annotation_type__name",
    "event_type__name",
    "item__item_type__name",
)


ordering_fields = ("created_on",)


class Filter(IrekuaUserFilter):
    annotation_type = filters.ModelChoiceFilter(
        queryset=AnnotationType.objects.all(),
        widget=get_autocomplete_widget(model=AnnotationType),
    )

    labels = filters.ModelChoiceFilter(
        queryset=Term.objects.all(),
        widget=get_autocomplete_widget(model=Term),
    )

    labels__term_type = filters.ModelChoiceFilter(
        queryset=TermType.objects.all(),
        widget=get_autocomplete_widget(model=TermType),
    )

    event_type = filters.ModelChoiceFilter(
        queryset=EventType.objects.all(),
        widget=get_autocomplete_widget(model=EventType),
    )

    item = filters.ModelChoiceFilter(
        queryset=Item.objects.all(),
        widget=get_autocomplete_widget(model=Item),
    )

    item__item_type = filters.ModelChoiceFilter(
        queryset=ItemType.objects.all(),
        widget=get_autocomplete_widget(model=ItemType),
    )

    class Meta:
        model = Annotation

        fields = {
            "annotation_type__name": ["exact", "icontains"],
            "labels__value": ["exact", "icontains"],
            "labels__term_type__name": ["exact", "icontains"],
            "event_type__name": ["exact", "icontains"],
            "item__item_type__name": ["exact", "icontains"],
        }
