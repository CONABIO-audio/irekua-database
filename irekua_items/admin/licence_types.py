from irekua_database.admin.base import IrekuaAdmin


class LicenceTypeAdmin(IrekuaAdmin):
    search_fields = [
        "name",
    ]

    list_display = [
        "id",
        "name",
        "can_view",
        "can_download",
        "can_view_annotations",
        "can_annotate",
        "created_on",
    ]

    list_display_links = [
        "id",
        "name",
    ]

    autocomplete_fields = [
        "metadata_schema",
    ]

    list_filter = [
        "can_view",
        "can_download",
        "can_view_annotations",
        "can_annotate",
        "can_vote_annotations",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "icon"),
                    "description",
                    ("document_template"),
                ),
            },
        ),
        ("Schemas", {"fields": (("metadata_schema"),)}),
        (
            "Permissions",
            {
                "fields": (
                    "years_valid_for",
                    (
                        "can_view",
                        "can_download",
                        "can_view_annotations",
                        "can_annotate",
                        "can_vote_annotations",
                    ),
                )
            },
        ),
    )
