from django_filters import rest_framework as filters

from irekua_geo.models import Locality
from irekua_geo.models import LocalityType
from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    'name',
    'description',
    'locality_type__name',
)


ordering_fields = (
    'created_on',
    'name',
)


class Filter(IrekuaFilter):
    locality_type = filters.ModelChoiceFilter(
        queryset=LocalityType.objects.all(),
        widget=get_autocomplete_widget(LocalityType),
    )

    is_part_of = filters.ModelChoiceFilter(
        queryset=Locality.objects.all(),
        widget=get_autocomplete_widget(Locality),
        method='filter_is_part_of',
    )

    has_part = filters.ModelChoiceFilter(
        queryset=Locality.objects.all(),
        widget=get_autocomplete_widget(Locality),
        method='filter_has_part',
    )

    class Meta:
        model = Locality

        fields = {
            'name': ['exact', 'icontains'],
        }

    def filter_is_part_of(self, queryset, name, value):
        if value is None:
            return queryset

        return queryset.filter(is_part_of=value)

    def filter_has_part(self, queryset, name, value):
        if value is None:
            return queryset

        return queryset.filter(is_part_of=value)
