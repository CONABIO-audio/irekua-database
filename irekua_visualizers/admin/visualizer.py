from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_visualizers.models import Visualizer
from irekua_visualizers.models import VisualizerVersion


class ItemTypeInline(admin.TabularInline):
    extra = 0

    model = Visualizer.item_types.through

    autocomplete_fields = ("item_type",)

    verbose_name = _("Item type")

    verbose_name_plural = _("Item types")


class VersionInline(admin.TabularInline):
    extra = 0

    model = VisualizerVersion

    verbose_name = _("Version")

    verbose_name_plural = _("Versions")


class VisualizerAdmin(IrekuaAdmin):
    search_fields = ["name", "description"]

    list_display = (
        "id",
        "__str__",
        "website",
        "created_on",
    )

    list_display_links = (
        "id",
        "__str__",
    )

    list_filter = ("item_types",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "website"),
                    ("description",),
                )
            },
        ),
    )

    inlines = [
        VersionInline,
        ItemTypeInline,
    ]
