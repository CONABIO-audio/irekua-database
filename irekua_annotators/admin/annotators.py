from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_annotators import models


class VersionsInline(admin.TabularInline):
    extra = 0

    model = models.AnnotatorVersion

    verbose_name = _("Version")

    verbose_name_plural = _("Versions")

    autocomplete_fields = ("configuration_schema",)

    fields = (
        "version",
        "configuration_schema",
    )


class AnnotatorAdmin(IrekuaAdmin):
    search_fields = [
        "name",
        "annotation_type__name",
    ]

    list_display = [
        "id",
        "__str__",
        "annotation_type",
        "created_on",
    ]

    list_display_links = [
        "id",
        "__str__",
    ]

    autocomplete_fields = [
        "annotation_type",
    ]

    list_filter = [
        "annotation_type",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "name",
                        "annotation_type",
                    ),
                    (
                        "website",
                        "logo",
                    ),
                )
            },
        ),
    )

    inlines = [
        VersionsInline,
    ]
