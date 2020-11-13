from irekua_database.models import Institution
from irekua_database.filters.base import IrekuaFilter


search_fields = (
    "institution_name",
    "institution_code",
)


ordering_fields = (
    "created_on",
    "institution_name",
    "institution_code",
)


class Filter(IrekuaFilter):
    class Meta:
        model = Institution

        fields = {
            "institution_name": ["exact", "icontains"],
            "institution_code": ["exact", "icontains"],
            "country": ["exact"],
        }
