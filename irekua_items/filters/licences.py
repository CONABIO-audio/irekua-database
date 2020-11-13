from django_filters import rest_framework as filters

from irekua_items.models import Licence
from irekua_items.models import LicenceType
from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    'name',
    'description',
)


ordering_fields = (
    'created_on',
    'name',
)


class Filter(IrekuaFilter):
    licence_type = filters.ModelChoiceFilter(
        queryset=LicenceType.objects.all(),
        widget=get_autocomplete_widget(model=LicenceType),
    )

    class Meta:
        model = Licence

        fields = {
            'licence_type__name': ['exact', 'icontains'],
            'is_active': ['exact'],
            'licence_type__years_valid_for': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'licence_type__can_view': ['exact'],
            'licence_type__can_download': ['exact'],
            'licence_type__can_view_annotations': ['exact'],
            'licence_type__can_annotate': ['exact'],
            'licence_type__can_vote_annotations': ['exact'],
        }
