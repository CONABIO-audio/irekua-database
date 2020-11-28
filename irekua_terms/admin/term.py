from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_terms.models import Entailment
from irekua_terms.models import Synonym


class SynonymInline(admin.TabularInline):
    extra = 0

    model = Synonym
    fk_name = "source"

    autocomplete_fields = [
        "target",
    ]

    verbose_name = _("Synonym")
    verbose_name_plural = _("Synonyms")

    classes = ("collapse",)


class EntailmentInline(admin.TabularInline):
    extra = 0

    model = Entailment
    fk_name = "source"

    autocomplete_fields = [
        "target",
    ]

    verbose_name = _("Entailment")
    verbose_name_plural = _("Entailments")

    classes = ("collapse",)


class TermAdmin(IrekuaAdmin):

    list_display = (
        "id",
        "value",
        "scope",
        "term_type",
        "created_on",
    )

    list_filter = [
        "term_type",
    ]

    list_display_links = [
        "id",
        "value",
    ]

    search_fields = [
        "term_type__name",
        "value",
        "scope",
    ]

    autocomplete_fields = [
        "term_type",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("term_type", "value"),
                    "description",
                    ("scope", "url"),
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": ("metadata",),
                "classes": ("collapse",),
            },
        ),
    )

    inlines = [
        SynonymInline,
        EntailmentInline,
    ]
