from django_filters import rest_framework as filters

from irekua_collections.models import Collection
from irekua_collections.models import CollectionType
from irekua_database.models import User
from irekua_database.models import Institution
from irekua_database.filters import IrekuaUserFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "name",
    "collection_type__name",
)


ordering_fields = (
    "created_on",
    "name",
    "collection_type__name",
)


class Filter(IrekuaUserFilter):
    collection_type = filters.ModelChoiceFilter(
        queryset=CollectionType.objects.all(),
        widget=get_autocomplete_widget(model=CollectionType),
    )

    institutions = filters.ModelChoiceFilter(
        queryset=Institution.objects.all(),
        widget=get_autocomplete_widget(model=Institution),
    )

    users = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=get_autocomplete_widget(model=User),
    )

    administrators = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=get_autocomplete_widget(model=User),
    )

    class Meta:
        model = Collection

        fields = {
            "name": ["exact", "icontains"],
            "is_open": ["exact"],
        }
