from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin


class CollectionLicenceAdmin(IrekuaUserAdmin):
    search_fields = [
        "collection__name",
        "collection__collection_type__name",
        "licence_type__name",
        "created_by__username",
    ]

    list_display = [
        "id",
        "collection",
        "licence_type",
        "is_active",
        "created_by",
        "created_on",
    ]

    list_display_links = [
        "id",
    ]

    list_filter = [
        "is_active",
        "collection",
        "licence_type",
        "collection__collection_type",
    ]

    autocomplete_fields = [
        "collection",
        "licence_type",
    ]

    readonly_fields = [
        *IrekuaUserAdmin.readonly_fields,
        "is_active",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("collection", "licence_type"),
                    "document",
                )
            },
        ),
        (
            _("Additional Metadata"),
            {"fields": (("metadata", "collection_metadata"),)},
        ),
        (_("Active"), {"fields": ("is_active",)}),
    )
