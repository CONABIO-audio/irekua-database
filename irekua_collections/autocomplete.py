from dal import autocomplete

from irekua_collections.models import CollectionType
from irekua_collections.models import Collection
from irekua_collections.models import DeploymentType
from irekua_collections.models import SamplingEventType
from irekua_database.autocomplete import register_autocomplete


urlpatterns = []


@register_autocomplete(DeploymentType, urlpatterns)
class DeploymentTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = DeploymentType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(SamplingEventType, urlpatterns)
class SamplingEventTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SamplingEventType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(CollectionType, urlpatterns)
class CollectionTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CollectionType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(Collection, urlpatterns)
class CollectionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Collection.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
