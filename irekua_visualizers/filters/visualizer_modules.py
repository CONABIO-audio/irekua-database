from django_filters import rest_framework as filters

from irekua_visualizers.models import VisualizerModule
from irekua_visualizers.models import VisualizerVersion
from irekua_items.models import ItemType
from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "javascript_file",
    "is_active",
)


ordering_fields = (
    "javascript_file",
)


class Filter(IrekuaFilter):
    visualizer_version__visualizer__item_types = filters.ModelChoiceFilter(
        queryset=ItemType.objects.all(),
        widget=get_autocomplete_widget(model=ItemType),
    )

    class Meta:
        model = VisualizerModule

        fields = {
            "visualizer_version__visualizer__item_types__name": ["exact", "icontains"],
            "visualizer_version__visualizer__item_types__id": ["exact", "icontains"],
        }
