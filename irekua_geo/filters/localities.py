from django_filters import rest_framework as filters
from django.utils.translation import gettext as _
from django.contrib.gis import forms

import django_filters
from irekua_geo.models import Locality
from irekua_geo.models import LocalityType
from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "name",
    "description",
    "locality_type__name",
)


ordering_fields = (
    "created_on",
    "name",
)


class PointFilter(django_filters.Filter):
    field_class = forms.GeometryField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", forms.TextInput)
        super().__init__(*args, **kwargs)


class Filter(IrekuaFilter):
    locality_type = filters.ModelChoiceFilter(
        queryset=LocalityType.objects.all(),
        widget=get_autocomplete_widget(LocalityType),
    )

    is_contained_in_locality = filters.ModelChoiceFilter(
        queryset=Locality.objects.all(),
        widget=get_autocomplete_widget(Locality),
        method="filter_is_part_of",
        label=_("Is contained"),
        help_text=_("Only show localities that belong to this locality"),
    )

    contains_locality = filters.ModelChoiceFilter(
        queryset=Locality.objects.all(),
        widget=get_autocomplete_widget(Locality),
        method="filter_has_part",
        label=_("Contains"),
        help_text=_("Only show localities that contain this locality"),
    )

    contains_point = PointFilter(
        method="filter_contains_point",
        label=_("Contains point"),
        help_text=_("Only show localities that contain this point"),
    )

    class Meta:
        model = Locality

        fields = {
            "name": ["exact", "icontains"],
        }

    def filter_is_part_of(self, queryset, name, value):
        if value is None:
            return queryset

        return queryset.filter(is_part_of=value)

    def filter_has_part(self, queryset, name, value):
        if value is None:
            return queryset

        return queryset.filter(is_part_of=value)

    def filter_contains_point(self, queryset, name, value):
        if value is None:
            return queryset

        return queryset.filter(geometry__contains=value)
