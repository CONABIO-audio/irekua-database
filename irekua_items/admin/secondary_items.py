from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin


class SecondaryItemAdmin(IrekuaAdmin):
    search_fields = [
        "item_type__name",
        "item__id",
        "id",
    ]

    list_display = [
        "id",
        "item",
        "item_type",
        "created_on",
    ]

    list_display_links = [
        "id",
    ]

    autocomplete_fields = [
        "item",
        "item_type",
    ]

    list_filter = [
        "item_type",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("item", "item_type"),
                    "item_file",
                )
            },
        ),
        (_("Item info"), {"fields": (("hash", "media_info"),)}),
    )
