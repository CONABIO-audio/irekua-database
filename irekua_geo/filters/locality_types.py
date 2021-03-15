from irekua_geo.models import LocalityType
from irekua_database.filters import IrekuaFilter


search_fields = (
    "name",
    "description",
    "source",
)


ordering_fields = ("created_on",)


class Filter(IrekuaFilter):
    class Meta:
        model = LocalityType

        fields = {
            "name": ["exact", "icontains"],
            "source": ["exact", "icontains"],
            "original_datum": ["exact", "icontains"],
            "publication_date": ["exact", "lt", "lte", "gt", "gte"],
        }
