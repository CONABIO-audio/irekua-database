from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from irekua_database.autocomplete import get_autocomplete_widget


class IrekuaFilter(filters.FilterSet):
    created_on__lt = filters.DateTimeFilter(
        field_name="created_on",
        lookup_expr="lt",
        label=_("Created before than"),
        widget=forms.DateTimeInput,
    )

    created_on__gt = filters.DateTimeFilter(
        field_name="created_on",
        lookup_expr="gt",
        label=_("Created after than"),
        widget=forms.DateTimeInput,
    )

    modified_on__lt = filters.DateTimeFilter(
        field_name="modified_on",
        lookup_expr="lt",
        label=_("Modified before than"),
        widget=forms.DateTimeInput,
    )

    modified_on__gt = filters.DateTimeFilter(
        field_name="modified_on",
        lookup_expr="gt",
        label=_("Modified after than"),
        widget=forms.DateTimeInput,
    )


class IrekuaUserFilter(IrekuaFilter):
    created_by = filters.ModelChoiceFilter(
        queryset=get_user_model().objects.all(),
        widget=get_autocomplete_widget(model=get_user_model()),
    )

    owns = filters.BooleanFilter(
        label=_("mine"),
        help_text=_("Filter elements created by user"),
        method="filter_owns",
    )

    # pylint: disable=no-self-use
    def filter_owns(self, queryset, name, value):
        if value is None:
            return queryset

        request = getattr(self, "request", None)
        if request is None:
            return queryset

        return queryset.filter(created_by=request.user)