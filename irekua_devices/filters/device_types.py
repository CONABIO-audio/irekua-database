from django_filters import rest_framework as filters

from irekua_devices.models import DeviceType
from irekua_items.models import MimeType
from irekua_database.filters import IrekuaFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "name",
    "description",
)


ordering_fields = (
    "created_on",
    "name",
)


class Filter(IrekuaFilter):
    mime_types = filters.ModelChoiceFilter(
        queryset=MimeType.objects.all(),
        widget=get_autocomplete_widget(model=MimeType),
    )

    class Meta:
        model = DeviceType

        fields = {
            "name": ["exact", "icontains"],
            "mime_types__mime_type": ["exact", "icontains"],
        }
