from django_filters import rest_framework as filters

from irekua_collections.models import CollectionSite
from irekua_collections.models import Collection
from irekua_collections.models import CollectionType
from irekua_geo.models import SiteType
from irekua_geo.models import SiteDescriptor
from irekua_geo.models import SiteDescriptorType
from irekua_geo.models import Site
from irekua_database.filters import IrekuaUserFilter
from irekua_database.autocomplete import get_autocomplete_widget


search_fields = (
    "collection_name",
    "site__name",
)


ordering_fields = (
    "created_on",
    "collection_name",
    "site__name",
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

    site = filters.ModelChoiceFilter(
        queryset=Site.objects.all(),
        widget=get_autocomplete_widget(model=Site),
    )

    site_type = filters.ModelChoiceFilter(
        queryset=SiteType.objects.all(),
        widget=get_autocomplete_widget(model=SiteType),
    )

    site_descriptors = filters.ModelChoiceFilter(
        queryset=SiteDescriptor.objects.all(),
        widget=get_autocomplete_widget(model=SiteDescriptor),
    )

    descriptor_type = filters.ModelChoiceFilter(
        queryset=SiteDescriptorType.objects.all(),
        field_name="site_descriptors__descriptor_type",
        widget=get_autocomplete_widget(model=SiteDescriptorType),
    )

    parent_site = filters.ModelChoiceFilter(
        queryset=CollectionSite.objects.all(),
        widget=get_autocomplete_widget(model=CollectionSite),
    )

    parent_parent_site = filters.ModelChoiceFilter(
        queryset=CollectionSite.objects.all(),
        widget=get_autocomplete_widget(model=CollectionSite),
        field_name="parent_site__parent_site",
    )

    parent_site_type = filters.ModelChoiceFilter(
        queryset=SiteType.objects.all(),
        field_name="parent_site__site_type",
        widget=get_autocomplete_widget(model=SiteType),
    )

    class Meta:
        model = CollectionSite

        fields = {
            "collection_name": ["exact", "icontains"],
            "collection__name": ["exact", "icontains"],
            "site_type__name": ["exact", "icontains"],
        }
