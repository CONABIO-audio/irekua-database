from dal import autocomplete

from irekua_geo.models import LocalityType
from irekua_geo.models import Locality
from irekua_geo.models import SiteDescriptorType
from irekua_geo.models import SiteType
from irekua_geo.models import SiteDescriptor
from irekua_geo.models import Site
from irekua_database.autocomplete import register_autocomplete


urlpatterns = []


@register_autocomplete(LocalityType, urlpatterns)
class LocalityTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = LocalityType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(Locality, urlpatterns)
class LocalityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Locality.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(SiteDescriptorType, urlpatterns)
class SiteDescriptorTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SiteDescriptorType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(SiteType, urlpatterns)
class SiteTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SiteType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(SiteDescriptor, urlpatterns)
class SiteDescriptorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SiteDescriptor.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(Site, urlpatterns)
class SiteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Site.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
