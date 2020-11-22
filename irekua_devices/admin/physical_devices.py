from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin


class PhysicalDeviceAdmin(IrekuaAdmin):
    search_fields = [
        "name",
        "serial_number",
        "device__device_type__name",
        "device__brand__name",
        "device__model",
    ]

    list_display = [
        "id",
        "name",
        "serial_number",
        "device",
        "created_by",
        "created_on",
    ]

    list_display_links = ["id", "name", "serial_number"]

    list_filter = [
        "device__device_type",
        "device__brand",
    ]

    autocomplete_fields = ["device"]

    fieldsets = (
        (None, {"fields": (("name", "device"), "serial_number")}),
        (
            _("Additional Metadata"),
            {
                "fields": (
                    "device_type_metadata",
                    "device_metadata",
                ),
            },
        ),
    )
