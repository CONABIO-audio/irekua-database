from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin


class DeploymentAdmin(IrekuaUserAdmin):
    search_fields = [
        "sampling_event__collection__name",
        "sampling_event__collection_site__collection_name",
        "collection_device__collection_name",
        "collection_device__physical_device__name",
        "sampling_event__collection_site__site__name",
    ]

    list_display = [
        "id",
        "__str__",
        "collection",
        "sampling_event",
        "collection_device",
        "deployment_type",
        "deployed_on",
        "recovered_on",
        "created_by",
        "created_on",
    ]

    list_display_links = [
        "id",
        "__str__",
    ]

    list_filter = [
        "sampling_event__collection",
        "sampling_event__collection__collection_type",
        "deployment_type",
    ]

    autocomplete_fields = [
        "sampling_event",
        "deployment_type",
        "collection_device",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("sampling_event", "deployment_type"),
                    "collection_device",
                    "commentaries",
                )
            },
        ),
        (_("Dates"), {"fields": (("deployed_on", "recovered_on"),)}),
        (
            _("Position"),
            {
                "fields": (
                    ("latitude", "longitude", "altitude"),
                    "geo_ref",
                ),
            },
        ),
        (_("Configuration"), {"fields": ("configuration",)}),
        (
            _("Additional Metadata"),
            {
                "fields": (("metadata", "collection_metadata"),),
            },
        ),
    )
