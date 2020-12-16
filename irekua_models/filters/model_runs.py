from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from irekua_database.autocomplete import get_autocomplete_widget
from irekua_database.filters import IrekuaFilter
from irekua_items.models import Item
from irekua_items.models import ItemType
from irekua_models.models import Model
from irekua_models.models import ModelRun
from irekua_models.models import ModelVersion


search_fields = (
    "model_version__model__name",
    "model_version__version",
)


ordering_fields = (
    "created_on",
    "item__captured_on",
    "model_version__version",
)


class Filter(IrekuaFilter):
    item = filters.ModelChoiceFilter(
        queryset=Item.objects.all(),
        widget=get_autocomplete_widget(model=Item),
    )

    item_type = filters.ModelChoiceFilter(
        queryset=ItemType.objects.all(),
        field_name="item__item_type",
        label=_("Item type"),
        widget=get_autocomplete_widget(model=ItemType),
    )

    model_version = filters.ModelChoiceFilter(
        queryset=ModelVersion.objects.all(),
        widget=get_autocomplete_widget(model=ModelVersion),
    )

    model = filters.ModelChoiceFilter(
        queryset=Model.objects.all(),
        field_name="model_version__model",
        label=_("Model"),
        widget=get_autocomplete_widget(model=Model),
    )

    class Meta:
        model = ModelRun

        fields = {}
