from irekua_database.admin.base import IrekuaUserAdmin


class ModelVersionAdmin(IrekuaUserAdmin):
    search_fields = [
        "model__name",
        "version",
    ]

    list_display = [
        "id",
        "__str__",
        "model",
        "version",
        "created_by",
        "created_on",
    ]

    list_display_links = [
        "id",
        "__str__",
    ]

    autocomplete_fields = [
        "model",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "model",
                        "version",
                    ),
                )
            },
        ),
    )
