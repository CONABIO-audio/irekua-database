from django_filters import rest_framework as filters

from irekua_collections.models import SamplingEventType
from irekua_collections.models import DeploymentType
from irekua_items.models import ItemType
from irekua_geo.models import SiteType

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
    deployment_types = filters.ModelChoiceFilter(
        queryset=DeploymentType.objects.all(),
        widget=get_autocomplete_widget(model=DeploymentType),
    )

    item_types = filters.ModelChoiceFilter(
        queryset=ItemType.objects.all(), widget=get_autocomplete_widget(model=ItemType)
    )

    site_types = filters.ModelChoiceFilter(
        queryset=SiteType.objects.all(), widget=get_autocomplete_widget(model=SiteType)
    )

    class Meta:
        model = SamplingEventType

        fields = {
            "name": ["exact", "icontains"],
            "restrict_deployment_types": ["exact"],
            "deployment_types__name": ["exact", "icontains"],
            "restrict_item_types": ["exact"],
            "item_types__name": ["exact", "icontains"],
            "restrict_site_types": ["exact"],
            "site_types__name": ["exact", "icontains"],
            "restrict_deployment_positions": ["exact"],
            "deployment_distance": ["exact", "lt", "gt", "lte", "gte"],
        }
