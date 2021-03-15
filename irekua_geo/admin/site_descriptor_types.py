from irekua_database.admin.base import IrekuaAdmin


class SiteDescriptorTypeAdmin(IrekuaAdmin):
    search_fields = [
        "name",
    ]

    list_display = [
        "id",
        "name",
        "created_on",
    ]

    list_display_links = [
        "id",
        "name",
    ]

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
                    "source",
                ),
            },
        ),
        ("Schemas", {"fields": (("metadata_schema"),)}),
    )
