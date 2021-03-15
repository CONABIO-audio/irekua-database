from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_annotations.models import EventType


class TermTypesInline(admin.TabularInline):
    extra = 0
    model = EventType.term_types.through
    autocomplete_fields = ("termtype",)
    verbose_name = _("Term type")
    verbose_name_plural = _("Term types")


class ShouldImplyInline(admin.TabularInline):
    extra = 0
    model = EventType.should_imply.through
    autocomplete_fields = ("term",)
    verbose_name = _("Should imply")
    verbose_name_plural = _("Should imply")


class AnnotationTypeInline(admin.TabularInline):
    extra = 0
    model = EventType.annotation_types.through
    autocomplete_fields = ("annotationtype",)
    verbose_name = _("Annotation type")
    verbose_name_plural = _("Annotation types")


class EventTypeAdmin(IrekuaAdmin):
    search_fields = ["name"]

    autocomplete_fields = [
        "should_imply",
        "term_types",
        "metadata_schema",
    ]

    list_display = (
        "id",
        "name",
        "restrict_annotation_types",
        "created_on",
    )

    list_display_links = ("id", "name")

    list_filter = [
        "restrict_annotation_types",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "icon"),
                    "description",
                ),
            },
        ),
        ("Schemas", {"fields": (("metadata_schema"),)}),
        (
            "Restrictions",
            {
                "fields": (("restrict_annotation_types",),),
            },
        ),
    )

    inlines = [
        TermTypesInline,
        ShouldImplyInline,
        AnnotationTypeInline,
    ]
