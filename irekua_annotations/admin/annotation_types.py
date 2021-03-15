from irekua_database.admin.base import IrekuaAdmin


class AnnotationTypeAdmin(IrekuaAdmin):
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
        "annotation_schema",
        "metadata_schema",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "icon"),
                    "description",
                )
            },
        ),
        ("Schemas", {"fields": (("annotation_schema", "metadata_schema"),)}),
    )
