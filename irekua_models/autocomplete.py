from django.db.models import Q
from dal import autocomplete

from irekua_models.models import Model
from irekua_models.models import ModelVersion
from irekua_models.models import ModelRun
from irekua_database.autocomplete import register_autocomplete


urlpatterns = []


@register_autocomplete(Model, urlpatterns)
class ModelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Model.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(ModelVersion, urlpatterns)
class ModelVersionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ModelVersion.objects.all()

        if self.q:
            qs = qs.filter(
                Q(model__name__istartswith=self.q)
                | Q(version__istartswith=self.q)
            )

        return qs


@register_autocomplete(ModelRun, urlpatterns)
class ModelRunAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ModelRun.objects.all()

        if self.q:
            qs = qs.filter(
                Q(model_version__model__name__istartswith=self.q)
                | Q(model_version__version__istartswith=self.q)
                | Q(item__id__istartswith=self.q)
            )

        return qs
