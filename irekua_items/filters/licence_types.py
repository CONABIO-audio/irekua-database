from irekua_items.models import LicenceType
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
        model = LicenceType

        fields = {
            'name': ['exact', 'icontains'],
            'years_valid_for': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'can_view': ['exact'],
            'can_download': ['exact'],
            'can_view_annotations': ['exact'],
            'can_annotate': ['exact'],
            'can_vote_annotations': ['exact'],
        }
