from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_terms.models import EntailmentType


class EntailmentTypeInline(admin.TabularInline):
    extra = 0
    model = EntailmentType
    fk_name = "source_type"
    autocomplete_fields = ("target_type",)
    verbose_name = _("Entailment")
    verbose_name_plural = _("Entailments")
    classes = ("collapse",)


class TermTypeAdmin(IrekuaAdmin):
    search_fields = ["name"]

    list_display = (
        "id",
        "name",
        "is_categorical",
        "is_integer",
        "is_numerical",
        "is_boolean",
        "created_on",
    )

    list_filter = [
        "is_categorical",
        "is_integer",
        "is_numerical",
        "is_boolean",
    ]

    list_display_links = ("id", "name")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "icon"),
                    "description",
                    (
                        "is_categorical",
                        "is_integer",
                        "is_numerical",
                        "is_boolean",
                    ),
                ),
            },
        ),
        (
            "Additional metadata",
            {
                "classes": ("collapse",),
                "fields": (("metadata_schema", "synonym_metadata_schema"),),
            },
        ),
    )

    inlines = [
        EntailmentTypeInline,
    ]
