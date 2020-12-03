from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from irekua_database.admin.base import IrekuaUserAdmin

from irekua_geo.models import Site


class LocalitiesInline(admin.TabularInline):
    extra = 0

    model = Site.localities.through

    autocomplete_fields = ("locality",)

    verbose_name = _("Locality")

    verbose_name_plural = _("Localities")


class SiteAdmin(IrekuaUserAdmin):
    search_fields = [
        "name",
        "locality__name",
    ]

    list_display = [
        "id",
        "name",
        "geometry_type",
        "created_on",
    ]

    list_display_links = [
        "id",
        "name",
    ]

    list_filter = [
        "created_on",
    ]

    readonly_fields = [
        *IrekuaUserAdmin.readonly_fields,
        "geom",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (("name", "geometry_type"),),
            },
        ),
        (
            None,
            {
                "fields": ("geom",),
            },
        ),
    )

    inlines = [
        LocalitiesInline,
    ]
