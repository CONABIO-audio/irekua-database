from dal import autocomplete

from irekua_annotations.models import AnnotationType
from irekua_annotations.models import EventType
from irekua_database.autocomplete import register_autocomplete


urlpatterns = []


@register_autocomplete(AnnotationType, urlpatterns)
class AnnotationTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = AnnotationType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(EventType, urlpatterns)
class EventTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = EventType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
