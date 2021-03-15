from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin


class CollectionDeviceAdmin(IrekuaUserAdmin):
    search_fields = [
        "collection_name",
        "collection__name",
        "physical_device__device__brand__name",
        "physical_device__device__model",
        "physical_device__serial_number",
    ]

    list_display = [
        "id",
        "__str__",
        "collection",
        "physical_device",
        "created_by",
        "created_on",
    ]

    list_filter = [
        "collection__collection_type",
        "physical_device__device__device_type",
        "physical_device__device__brand",
        "collection",
    ]

    list_display_links = [
        "id",
        "__str__",
    ]

    autocomplete_fields = [
        "collection",
        "physical_device",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("collection", "physical_device"),
                    "collection_name",
                )
            },
        ),
        (_("Additional Metadata"), {"fields": ("collection_metadata",)}),
    )
