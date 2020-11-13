from irekua_terms.models import TermType
from irekua_database.filters import IrekuaFilter


search_fields = (
    'name',
    'description',
)


ordering_fields = (
    'created_on',
    'name',
)


class Filter(IrekuaFilter):
    class Meta:
        model = TermType

        fields = {
            'name': ['exact', 'icontains'],
            'is_categorical': ['exact'],
            'is_numerical': ['exact'],
            'is_boolean': ['exact'],
            'is_integer': ['exact'],
        }
