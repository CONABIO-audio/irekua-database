from dal import autocomplete
from django.db.models import Q

from irekua_collections.models import CollectionType
from irekua_collections.models import Collection
from irekua_collections.models import CollectionSite
from irekua_collections.models import CollectionDevice
from irekua_collections.models import DeploymentType
from irekua_collections.models import SamplingEventType
from irekua_collections.models import SamplingEvent
from irekua_collections.models import Deployment
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


@register_autocomplete(CollectionSite, urlpatterns)
class CollectionSiteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CollectionSite.objects.all()

        if self.q:
            qs = qs.filter(collection_name__istartswith=self.q)

        return qs


@register_autocomplete(SamplingEvent, urlpatterns)
class SamplingEventAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SamplingEvent.objects.all()

        if self.q:
            qs = qs.filter(collection_site__collection_name__icontains=self.q)

        return qs


@register_autocomplete(CollectionDevice, urlpatterns)
class CollectionDeviceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CollectionDevice.objects.all()

        if self.q:
            qs = qs.filter(collection_name__icontains=self.q)

        return qs


@register_autocomplete(Deployment, urlpatterns)
class DeploymentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Deployment.objects.all()

        if not self.q:
            return qs

        device_name = Q(collection_device__collection_name__icontains=self.q)
        site_name = Q(
            sampling_event__collection_site__collection_name__icontains=self.q
        )

        return qs.filter(device_name | site_name)
