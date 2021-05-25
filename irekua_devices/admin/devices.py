from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin


class DeviceAdmin(IrekuaAdmin):
    search_fields = [
        "device_type__name",
        "brand__name",
        "model",
    ]

    list_display = [
        "id",
        "model",
        "brand",
        "device_type",
        "created_on",
    ]

    list_display_links = [
        "id",
        "model",
    ]

    list_filter = [
        "device_type",
        "brand",
    ]

    autocomplete_fields = [
        "device_type",
        "brand",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("device_type", "brand"),
                    "model",
                )
            },
        ),
        (
            _("Schemas"),
            {"fields": (("metadata_schema", "configuration_schema"),)},
        ),
    )
