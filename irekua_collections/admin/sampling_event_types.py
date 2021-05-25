from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaAdmin
from irekua_collections.models import SamplingEventType


class SiteTypeInline(admin.TabularInline):
    extra = 0

    model = SamplingEventType.site_types.through

    autocomplete_fields = ("sitetype",)

    verbose_name = _("Site type")

    verbose_name_plural = _("Site types")


class DeploymentTypeInline(admin.TabularInline):
    extra = 0

    model = SamplingEventType.deployment_types.through

    autocomplete_fields = ("deploymenttype",)

    verbose_name = _("Deployment type")

    verbose_name_plural = _("Deployment types")


class SubSamplingEventTypesInline(admin.TabularInline):
    extra = 0

    model = SamplingEventType.subsampling_event_types.through

    fk_name = "from_samplingeventtype"

    autocomplete_fields = ("to_samplingeventtype",)

    verbose_name = _("Subsampling event type")

    verbose_name_plural = _("Subsampling event types")


class ItemTypeInline(admin.TabularInline):
    extra = 0

    model = SamplingEventType.item_types.through

    autocomplete_fields = ("itemtype",)

    verbose_name = _("Item type")

    verbose_name_plural = _("Item types")


class SamplingEventTypeAdmin(IrekuaAdmin):
    search_fields = ("name",)

    list_display = (
        "id",
        "name",
        "restrict_site_types",
        "restrict_deployment_types",
        "can_have_subsampling_events",
        "restrict_subsampling_event_types",
        "created_on",
    )

    list_display_links = (
        "id",
        "name",
    )

    list_filter = ("restrict_site_types", "restrict_deployment_types")

    autocomplete_fields = [
        "metadata_schema",
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
                "fields": (
                    (
                        "restrict_site_types",
                        "restrict_deployment_types",
                        "restrict_item_types",
                    ),
                    ("restrict_deployment_positions", "deployment_distance"),
                    (
                        "can_have_subsampling_events",
                        "restrict_subsampling_event_types",
                    ),
                ),
            },
        ),
    )

    inlines = [
        SiteTypeInline,
        DeploymentTypeInline,
        ItemTypeInline,
        SubSamplingEventTypesInline,
    ]
