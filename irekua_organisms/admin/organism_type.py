from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_organisms.models import OrganismType


class TermTypeInline(admin.TabularInline):
    extra = 0

    model = OrganismType.term_types.through

    autocomplete_fields = ("termtype",)

    verbose_name = _("Term Type")

    verbose_name_plural = _("Term Types")


class ItemTypeInline(admin.TabularInline):
    extra = 0

    model = OrganismType.item_types.through

    autocomplete_fields = ("itemtype",)

    verbose_name = _("Item Type")

    verbose_name_plural = _("Item Types")


class OrganismTypeAdmin(IrekuaAdmin):
    search_fields = [
        "name",
    ]

    list_display = (
        "id",
        "__str__",
        "is_multi_organism",
        "restrict_item_types",
        "created_on",
    )

    list_display_links = (
        "id",
        "__str__",
    )

    list_filter = (
        "is_multi_organism",
        "created_on",
    )

    autocomplete_fields = ("term_types",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "icon"),
                    "description",
                    "is_multi_organism",
                )
            },
        ),
        (
            _("Identification"),
            {
                "fields": ("identification_info_schema",),
            },
        ),
        (_("Restrictions"), {"fields": ("restrict_item_types",)}),
    )

    inlines = [
        TermTypeInline,
        ItemTypeInline,
    ]
