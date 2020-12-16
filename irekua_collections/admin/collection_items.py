from django.utils.translation import gettext_lazy as _

from irekua_items.admin.items import ItemAdmin


class CollectionItemAdmin(ItemAdmin):
    search_fields = [
        "collection__name",
        *ItemAdmin.search_fields,
    ]

    list_display = [
        "id",
        "__str__",
        "item_type",
        "licence",
        "collection",
        "collection_site",
        "collection_device",
        "sampling_event",
        "deployment",
        "filesize",
        "captured_on",
        "created_by",
        "created_on",
    ]

    list_filter = [
        "collection",
        "collection_site__site_type",
        "sampling_event__sampling_event_type",
        "deployment__deployment_type",
        "collection_device__physical_device__device__device_type",
        *ItemAdmin.list_filter,
    ]

    autocomplete_fields = [
        "collection",
        "collection_site",
        "collection_device",
        "sampling_event",
        "deployment",
        *ItemAdmin.autocomplete_fields,
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("collection", "collection_device", "collection_site"),
                    ("sampling_event", "deployment"),
                    ("item_type", "licence"),
                    ("item_file",),
                )
            },
        ),
        (
            _("Item Info"),
            {
                "fields": (
                    ("hash", "filesize"),
                    "media_info",
                )
            },
        ),
        (
            _("Captured on"),
            {
                "fields": (
                    ("captured_on", "captured_on_timezone"),
                    (
                        "captured_on_year",
                        "captured_on_month",
                        "captured_on_day",
                    ),
                    (
                        "captured_on_hour",
                        "captured_on_minute",
                        "captured_on_second",
                    ),
                )
            },
        ),
        (
            _("Additional Metadata"),
            {
                "fields": ("metadata", "collection_metadata"),
            },
        ),
        (
            _("Source"),
            {
                "classes": ("collapse",),
                "fields": (("source", "source_foreign_key"),),
            },
        ),
    )