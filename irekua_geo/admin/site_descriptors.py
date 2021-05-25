from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin


class SiteDescriptorAdmin(IrekuaAdmin):
    search_fields = [
        "value",
        "descriptor_type__name",
    ]

    list_display = [
        "id",
        "value",
        "descriptor_type",
        "created_on",
    ]

    list_display_links = [
        "id",
        "value",
    ]

    list_filter = [
        "descriptor_type",
    ]

    autocomplete_fields = [
        "descriptor_type",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("descriptor_type", "value"),
                    "description",
                )
            },
        ),
        (_("Additional Metadata"), {"fields": (("metadata",),)}),
    )
