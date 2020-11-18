from django_filters import rest_framework as filters

from irekua_collections.models import CollectionUser
from irekua_collections.models import Collection
from irekua_collections.models import CollectionType
from irekua_database.models import User
from irekua_database.models import Role
from irekua_database.models import Institution
from irekua_database.filters import IrekuaUserFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "user__username",
    "user__first_name",
    "user__last_name",
    "user__email",
)


ordering_fields = (
    "created_on",
    "user__username",
    "user__first_name",
    "user__last_name",
    "user__email",
)


class Filter(IrekuaUserFilter):
    collection = filters.ModelChoiceFilter(
        queryset=Collection.objects.all(),
        widget=get_autocomplete_widget(model=Collection),
    )

    collection_type = filters.ModelChoiceFilter(
        queryset=CollectionType.objects.all(),
        field_name="collection__collection_type",
        widget=get_autocomplete_widget(model=CollectionType),
    )

    role = filters.ModelChoiceFilter(
        queryset=Role.objects.all(),
        widget=get_autocomplete_widget(model=Role),
    )

    user = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=get_autocomplete_widget(model=User),
    )

    institution = filters.ModelChoiceFilter(
        queryset=Institution.objects.all(),
        field_name="user__institutions",
        widget=get_autocomplete_widget(model=Institution),
    )

    class Meta:
        model = CollectionUser

        fields = {
            "user__username": ["exact", "icontains"],
            "user__first_name": ["exact", "icontains"],
            "user__last_name": ["exact", "icontains"],
            "user__email": ["exact", "icontains"],
        }
