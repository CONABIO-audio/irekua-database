from irekua_geo.models import SiteDescriptorType
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
        model = SiteDescriptorType

        fields = {
            'name': ['exact', 'icontains'],
            'source': ['exact', 'icontains'],
        }
