from django_filters import rest_framework as filters

from irekua_database.models import User
from irekua_database.models import Institution
from irekua_database.autocomplete import get_autocomplete_widget
from irekua_database.filters.base import IrekuaFilter


search_fields = (
    "username",
    "first_name",
    "last_name",
)


ordering_fields = (
    "created_on",
    "username",
    "first_name",
    "last_name",
)


class Filter(IrekuaFilter):
    institutions = filters.ModelChoiceFilter(
        queryset=Institution.objects.all(),
        widget=get_autocomplete_widget(model=Institution),
    )

    class Meta:
        model = User

        fields = {
            "username": ["exact", "icontains"],
            "first_name": ["exact", "icontains"],
            "last_name": ["exact", "icontains"],
        }
