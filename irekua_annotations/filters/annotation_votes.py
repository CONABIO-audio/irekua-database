from django_filters import rest_framework as filters

from irekua_annotations.models import AnnotationVote
from irekua_annotations.models import Annotation
from irekua_terms.models import Term
from irekua_terms.models import TermType
from irekua_database.filters import IrekuaUserFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "annotation__id",
    "created_by__username",
)


ordering_fields = (
    "created_on",
    "annotation",
)


class Filter(IrekuaUserFilter):
    annotation = filters.ModelChoiceFilter(
        queryset=Annotation.objects.all(),
        widget=get_autocomplete_widget(model=Annotation),
    )

    labels = filters.ModelChoiceFilter(
        queryset=Term.objects.all(), widget=get_autocomplete_widget(model=Term)
    )

    labels__term_type = filters.ModelChoiceFilter(
        queryset=TermType.objects.all(), widget=get_autocomplete_widget(model=TermType)
    )

    class Meta:
        model = AnnotationVote

        fields = {
            "incorrect_geometry": ["exact"],
            "labels__value": ["exact", "icontains"],
            "labels": ["isnull"],
        }
