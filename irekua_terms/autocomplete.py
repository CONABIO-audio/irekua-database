from dal import autocomplete

from irekua_terms.models import Term
from irekua_terms.models import TermType
from irekua_database.autocomplete import register_autocomplete


urlpatterns = []


@register_autocomplete(TermType, urlpatterns)
class TermTypesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = TermType.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@register_autocomplete(Term, urlpatterns)
class TermsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Term.objects.all()

        if self.q:
            qs = qs.filter(value__istartswith=self.q)

        return qs
