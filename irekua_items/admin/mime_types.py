from irekua_database.admin.base import IrekuaAdmin


class MimeTypeAdmin(IrekuaAdmin):
    search_fields = [
        "mime_type",
    ]

    list_display = [
        "id",
        "mime_type",
        "created_on",
    ]

    list_display_links = [
        "id",
        "mime_type",
    ]

    autocomplete_fields = [
        "media_info_type",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "mime_type",
                    "media_info_type",
                ),
            },
        ),
    )
