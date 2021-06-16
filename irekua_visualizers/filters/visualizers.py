from django_filters import rest_framework as filters

from irekua_visualizers.models import Visualizer
from irekua_items.models import ItemType
from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "name",
    "website",
)


ordering_fields = (
    "name",
)


class Filter(IrekuaFilter):
    item_types = filters.ModelChoiceFilter(
        queryset=ItemType.objects.all(),
        widget=get_autocomplete_widget(model=ItemType),
    )

    class Meta:
        model = Visualizer

        fields = {
            "item_types__name": ["exact", "icontains"],
            "name": ["exact"],
        }
