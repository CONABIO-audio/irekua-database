from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin


class SamplingEventAdmin(IrekuaUserAdmin):
    search_fields = [
        "sampling_event_type__name",
        "collection_site__collection_name",
        "collection__name",
        "collection__collection_type__name",
    ]

    list_display = [
        "id",
        "__str__",
        "collection_site",
        "collection",
        "sampling_event_type",
        "started_on",
        "ended_on",
        "created_by",
        "created_on",
    ]

    list_display_links = [
        "id",
        "__str__",
    ]

    list_filter = [
        "sampling_event_type",
        "collection",
        "collection__collection_type",
        "collection_site__site_type",
        "started_on",
        "ended_on",
    ]

    autocomplete_fields = [
        "collection",
        "collection_site",
        "sampling_event_type",
        "parent_sampling_event",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("collection", "sampling_event_type"),
                    ("collection_site", "parent_sampling_event"),
                    "commentaries",
                )
            },
        ),
        (
            _("Dates"),
            {
                "fields": (("started_on", "ended_on"),),
            },
        ),
        (
            _("Additional Metadata"),
            {
                "fields": (("metadata", "collection_metadata"),),
            },
        ),
    )
