from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin
from irekua_items.models import Item


class TagInline(admin.TabularInline):
    extra = 0

    model = Item.tags.through

    verbose_name = _("Tag")

    verbose_name_plural = _("Tags")

    autocomplete_fields = [
        "tag",
    ]


class ItemAdmin(IrekuaUserAdmin):
    search_fields = [
        "id",
        "item_type__name",
        "mime_type__name",
    ]

    list_display = [
        "id",
        "item_type",
        "mime_type",
        "filesize",
        "captured_on",
        "licence",
        "created_by",
        "created_on",
    ]

    list_filter = [
        "item_type",
        "mime_type",
        "licence__licence_type",
    ]

    list_display_links = [
        "id",
    ]

    autocomplete_fields = [
        "item_type",
        "source",
        "licence",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("item_type", "licence"),
                    "item_file",
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
                "fields": ("metadata",),
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

    inlines = [
        TagInline,
    ]
