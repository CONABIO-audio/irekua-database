from irekua_annotations.models import AnnotationType
from irekua_database.filters import IrekuaFilter


search_fields = (
    "name",
    "description",
)


ordering_fields = (
    "created_on",
    "name",
)


class Filter(IrekuaFilter):
    class Meta:
        model = AnnotationType

        fields = {
            "name": ["exact", "icontains"],
        }
