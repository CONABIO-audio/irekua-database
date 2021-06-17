from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin
from irekua_collections.models import CollectionSite


class SiteDescriptorForm(forms.ModelForm):
    class Meta:
        model = CollectionSite.site_descriptors.through
        fields = (
            "collectionsite",
            "sitedescriptor",
        )

    def clean_descriptor(self, collection_site, site_descriptor):
        try:
            collection_site.validate_descriptor(site_descriptor)

        except ValidationError as error:
            raise ValidationError({"sitedescriptor": error}) from error

    def check_unique_descriptor_per_type(
        self, collection_site, site_descriptor
    ):
        query = collection_site.site_descriptors.filter(
            descriptor_type=site_descriptor.descriptor_type
        ).exclude(pk=site_descriptor.pk)

        if query.exists():
            msg = _("Only one descriptor per descriptor type is valid")
            raise ValidationError({"sitedescriptor": msg})

    def clean(self):
        cleaned_data = super().clean()

        #  Do not validate if delete operation
        if cleaned_data["DELETE"]:
            return cleaned_data

        collection_site = cleaned_data["collectionsite"]
        site_descriptor = cleaned_data["sitedescriptor"]

        #  Check descriptor is valid for site type
        self.clean_descriptor(collection_site, site_descriptor)

        # Check no more than one descriptor per descriptor type
        # is used
        self.check_unique_descriptor_per_type(collection_site, site_descriptor)

        return cleaned_data


class SiteDescriptorInline(admin.TabularInline):
    extra = 0

    form = SiteDescriptorForm

    model = CollectionSite.site_descriptors.through

    verbose_name = _("Descriptor")

    verbose_name_plural = _("Descriptors")

    autocomplete_fields = [
        "sitedescriptor",
    ]


class AssociatedUserInline(admin.TabularInline):
    extra = 0

    model = CollectionSite.associated_users.through

    verbose_name = _("Associated user")

    verbose_name_plural = _("Associated users")

    autocomplete_fields = [
        "user",
    ]


class CollectionSiteAdmin(IrekuaUserAdmin):
    search_fields = [
        "collection_name",
        "collection__name",
        "collection__collection_type__name",
        "site__name",
        "site_type__name",
        "created_by__username",
    ]

    list_display = [
        "id",
        "__str__",
        "collection",
        "site",
        "site_type",
        "created_by",
        "created_on",
    ]

    list_display_links = [
        "id",
        "__str__",
    ]

    list_filter = [
        "site_type",
        "collection",
        "collection__collection_type",
    ]

    autocomplete_fields = [
        "collection",
        "site",
        "site_type",
        "parent_site",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("collection", "site_type"),
                    ("site", "collection_name"),
                )
            },
        ),
        (
            _("Additional Metadata"),
            {"fields": (("metadata", "collection_metadata"),)},
        ),
        (_("Site Hierarchy"), {"fields": ("parent_site",)}),
    )

    inlines = [
        SiteDescriptorInline,
        AssociatedUserInline,
    ]
