from dal import autocomplete

from irekua_schemas.models import Schema
from irekua_database.autocomplete import register_autocomplete


urlpatterns = []


@register_autocomplete(Schema, urlpatterns)
class SchemaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Schema.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
