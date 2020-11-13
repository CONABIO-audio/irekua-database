from django.db import models
from django_filters import rest_framework as filters

from irekua_terms.models import Entailment
from irekua_terms.models import Term
from irekua_terms.models import TermType
from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    'source__value',
    'target__value',
    'source__term_type__name',
    'target__term_type__name',
)


ordering_fields = (
    'created_on',
)


class Filter(IrekuaFilter):
    source = filters.ModelChoiceFilter(
        queryset=Term.objects.all(),
        widget=get_autocomplete_widget(model=Term),
    )

    target = filters.ModelChoiceFilter(
        queryset=Term.objects.all(),
        widget=get_autocomplete_widget(model=Term),
    )

    source__term_type = filters.ModelChoiceFilter(
        queryset=TermType.objects.all(),
        widget=get_autocomplete_widget(model=TermType),
    )

    target__term_type = filters.ModelChoiceFilter(
        queryset=TermType.objects.all(),
        widget=get_autocomplete_widget(model=TermType),
    )

    class Meta:
        model = Entailment

        fields = {
            'source__value': ['exact', 'icontains'],
            'target__value': ['exact', 'icontains'],
            'source__term_type__name': ['exact', 'icontains'],
            'target__term_type__name': ['exact', 'icontains'],
        }
