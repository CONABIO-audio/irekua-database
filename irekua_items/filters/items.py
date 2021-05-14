from django.utils.translation import gettext as _
from django_filters import rest_framework as filters

from irekua_database.models import User
from irekua_items.models import Item
from irekua_items.models import ItemType
from irekua_items.models import MimeType
from irekua_items.models import LicenceType
from irekua_items.models import Tag

from irekua_database.filters import IrekuaUserFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "item_type__name",
    "hash",
    "id",
)


ordering_fields = (
    "created_on",
    "captured_on",
    "filesize",
)


class Filter(IrekuaUserFilter):
    item_type = filters.ModelChoiceFilter(
        queryset=ItemType.objects.all(),
        widget=get_autocomplete_widget(model=ItemType),
    )

    mime_type = filters.ModelChoiceFilter(
        queryset=MimeType.objects.all(),
        widget=get_autocomplete_widget(model=MimeType),
    )

    licence_type = filters.ModelChoiceFilter(
        queryset=LicenceType.objects.all(),
        widget=get_autocomplete_widget(model=LicenceType),
        label=_("Licence type"),
        to_field_name="licence__licence_type",
    )

    tags = filters.ModelChoiceFilter(
        queryset=Tag.objects.all(),
        widget=get_autocomplete_widget(model=Tag),
    )

    created_by = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=get_autocomplete_widget(model=User),
    )

    class Meta:
        model = Item

        fields = {
            "captured_on": ["exact", "lt", "gt", "lte", "gte"],
            "filesize": ["exact", "lt", "gt", "lte", "gte"],
            "item_type__name": ["exact", "icontains"],
            "licence__is_active": ["exact"],
            "licence__licence_type__name": ["exact", "icontains"],
            "captured_on_year": ["exact", "lt", "gt", "lte", "gte"],
            "captured_on_month": ["exact", "lt", "gt", "lte", "gte"],
            "captured_on_day": ["exact", "lt", "gt", "lte", "gte"],
            "captured_on_hour": ["exact", "lt", "gt", "lte", "gte"],
            "captured_on_minute": ["exact", "lt", "gt", "lte", "gte"],
            "captured_on_second": ["exact", "lt", "gt", "lte", "gte"],
            "captured_on_timezone": ["exact", "icontains"],
        }
