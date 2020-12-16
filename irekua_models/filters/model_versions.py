from django_filters import rest_framework as filters

from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget
from irekua_models.models import ModelVersion
from irekua_models.models import Model


search_fields = (
    "model__name",
    "version",
)


ordering_fields = (
    "created_on",
    "version",
)


class Filter(IrekuaFilter):
    model = filters.ModelChoiceFilter(
        queryset=Model.objects.all(),
        widget=get_autocomplete_widget(model=Model),
    )

    class Meta:
        model = ModelVersion

        fields = {
            "version": ["exact", "icontains"],
        }
