from irekua_database.admin.base import IrekuaUserAdmin


class ModelRunAdmin(IrekuaUserAdmin):
    search_fields = [
        "model_version__model__name",
        "model_version__model",
        "item__item_type__name",
    ]

    list_display = [
        "id",
        "__str__",
        "model_version",
        "item",
        "created_by",
        "created_on",
    ]

    list_display_links = [
        "id",
        "__str__",
    ]

    autocomplete_fields = [
        "model_version",
        "item",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "model_version",
                        "item",
                    ),
                )
            },
        ),
    )
