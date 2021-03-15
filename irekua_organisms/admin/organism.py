from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin
from irekua_organisms.models import Organism


class LabelsInline(admin.TabularInline):
    extra = 0

    model = Organism.labels.through

    verbose_name = _("Label")

    verbose_name_plural = _("Labels")

    autocomplete_fields = ["term"]


class OrganismAdmin(IrekuaUserAdmin):
    search_fields = [
        "name",
        "organism_type__name",
        "collection__name",
    ]

    list_display = (
        "id",
        "__str__",
        "name",
        "collection",
        "organism_type",
        "created_by",
        "created_on",
    )

    list_display_links = (
        "id",
        "__str__",
        "name",
    )

    list_filter = (
        "collection",
        "organism_type",
        "collection__collection_type",
    )

    autocomplete_fields = ("collection", "organism_type")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("collection", "organism_type"),
                    "name",
                    "remarks",
                )
            },
        ),
        (
            _("Identification"),
            {
                "fields": ("identification_info",),
            },
        ),
        (
            _("Additional Metadata"),
            {
                "fields": (("metadata", "collection_metadata"),),
            },
        ),
    )
