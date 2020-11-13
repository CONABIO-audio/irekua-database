from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from irekua_terms.models import Term
from irekua_terms.models import TermType

from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget



search_fields = (
    'term_type__name',
    'value',
    'description',
)


ordering_fields = (
    'created_on',
    'value',
    'term_type',
)


class Filter(IrekuaFilter):
    term_type = filters.ModelChoiceFilter(
        queryset=TermType.objects.all(),
        widget=get_autocomplete_widget(model=TermType),
    )

    entails = filters.ModelChoiceFilter(
        queryset=Term.objects.all(),
        label=_('entails'),
        help_text=_('Only show terms that entail this term'),
        widget=get_autocomplete_widget(model=Term),
        method='filter_entails',
    )

    is_entailed_by = filters.ModelChoiceFilter(
        queryset=Term.objects.all(),
        label=_('is entailed by'),
        help_text=_('Only show terms that are entailed by this term'),
        widget=get_autocomplete_widget(model=Term),
        method='filter_is_entailed_by',
    )

    synonyms = filters.ModelChoiceFilter(
        queryset=Term.objects.all(),
        label=_('synonyms'),
        help_text=_('Only show terms that are synonymous with this term'),
        widget=get_autocomplete_widget(model=Term),
        method='filter_synonyms',
    )

    class Meta:
        model = Term
        fields = {
            'value': ['exact', 'icontains'],
            'term_type__name': ['exact', 'icontains'],
        }

    def filter_entails(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(entailment_source__target=value)

    def filter_is_entailed_by(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(entailment_target__source=value)

    def filter_synonyms(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(synonym_target__source=value)
