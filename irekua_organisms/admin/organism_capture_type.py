from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_organisms.models import OrganismCaptureType


class TermTypeInline(admin.TabularInline):
    extra = 0

    model = OrganismCaptureType.term_types.through

    autocomplete_fields = ("termtype",)

    verbose_name = _("Term Type")

    verbose_name_plural = _("Term Types")


class ItemTypeInline(admin.TabularInline):
    extra = 0

    model = OrganismCaptureType.item_types.through

    autocomplete_fields = ("itemtype",)

    verbose_name = _("Item Type")

    verbose_name_plural = _("Item Types")


class OrganismCaptureTypeAdmin(IrekuaAdmin):
    search_fields = ["name"]

    list_display = (
        "id",
        "__str__",
        "organism_type",
        "device_type",
        "restrict_item_types",
        "created_on",
    )

    list_display_links = (
        "id",
        "__str__",
    )

    autocomplete_fields = (
        "device_type",
        "organism_type",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "icon"),
                    "description",
                    ("device_type", "organism_type"),
                )
            },
        ),
        (_("Restrictions"), {"fields": ("restrict_item_types",)}),
    )

    inlines = [
        TermTypeInline,
        ItemTypeInline,
    ]
