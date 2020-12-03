from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_geo.models import SiteType


class SiteDescriptorTypeInline(admin.TabularInline):
    extra = 0

    model = SiteType.site_descriptor_types.through

    autocomplete_fields = ("sitedescriptortype",)

    verbose_name = _("Site descriptor type")

    verbose_name_plural = _("Site descriptor types")


class SubSiteTypeInline(admin.TabularInline):
    extra = 0

    model = SiteType.subsite_types.through

    fk_name = "to_sitetype"

    autocomplete_fields = ("from_sitetype",)

    verbose_name = _("Sub Site type")

    verbose_name_plural = _("Sub Site types")


class SiteTypeAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
    ]

    list_display = [
        "id",
        "name",
        "point_site",
        "linestring_site",
        "multilinestring_site",
        "multipoint_site",
        "multipolygon_site",
        "polygon_site",
        "can_have_subsites",
        "created_on",
    ]

    list_filter = [
        "point_site",
        "linestring_site",
        "multilinestring_site",
        "multipoint_site",
        "multipolygon_site",
        "polygon_site",
        "can_have_subsites",
        "restrict_subsite_types",
    ]

    list_display_links = [
        "id",
        "name",
    ]

    autocomplete_fields = ["metadata_schema"]

    fieldsets = (
        (
            None,
            {
                "fields": (("name", "icon"), "description"),
            },
        ),
        (_("Schemas"), {"fields": ("metadata_schema",)}),
        (
            _("Geometry Types"),
            {
                "fields": (
                    ("point_site", "linestring_site", "polygon_site"),
                    ("multipoint_site", "multilinestring_site", "multipolygon_site"),
                )
            },
        ),
        (
            _("Subsites"),
            {
                "fields": (("can_have_subsites", "restrict_subsite_types"),),
            },
        ),
    )

    inlines = [
        SiteDescriptorTypeInline,
        SubSiteTypeInline,
    ]
