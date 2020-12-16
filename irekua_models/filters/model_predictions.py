from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from irekua_annotations.filters import annotations
from irekua_models.models import ModelPrediction
from irekua_models.models import ModelVersion
from irekua_models.models import ModelRun
from irekua_models.models import Model
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    *annotations.search_fields,
    "model_version__model__name",
    "model_version__version",
)


ordering_fields = (
    *annotations.ordering_fields,
    "model_version__version",
)


class Filter(annotations.Filter):
    model_version = filters.ModelChoiceFilter(
        queryset=ModelVersion.objects.all(),
        widget=get_autocomplete_widget(model=ModelVersion),
    )

    model_run = filters.ModelChoiceFilter(
        queryset=ModelRun.objects.all(),
        widget=get_autocomplete_widget(model=ModelRun),
    )

    model = filters.ModelChoiceFilter(
        queryset=Model.objects.all(),
        field_name="model_version__model",
        label=_("Model"),
        widget=get_autocomplete_widget(model=Model),
    )

    class Meta(annotations.Filter.Meta):
        model = ModelPrediction
