from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_collections.models import DeploymentType


class ItemTypeInline(admin.TabularInline):
    extra = 0

    model = DeploymentType.item_types.through

    autocomplete_fields = ("itemtype",)

    verbose_name = _("Item type")

    verbose_name_plural = _("Item types")


class DeploymentTypeAdmin(IrekuaAdmin):
    search_fields = (
        "name",
        "device_type__name",
    )

    list_display = (
        "id",
        "name",
        "device_type",
        "restrict_item_types",
        "created_on",
    )

    list_display_links = ("id", "name")

    list_filter = (
        "device_type",
        "restrict_item_types",
    )

    autocomplete_fields = ("metadata_schema",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "icon"),
                    "description",
                    "device_type",
                ),
            },
        ),
        ("Schemas", {"fields": (("metadata_schema"),)}),
        (
            "Restrictions",
            {
                "fields": (("restrict_item_types",),),
            },
        ),
    )

    inlines = [
        ItemTypeInline,
    ]
