from irekua_database.admin.base import IrekuaUserAdmin


class ModelPredictionAdmin(IrekuaUserAdmin):
    search_fields = [
        "pk",
    ]

    list_display = [
        "id",
        "item",
        "event_type",
        "annotation_type",
        "certainty",
        "created_by",
        "created_on",
    ]

    list_filter = [
        "event_type",
        "annotation_type",
    ]

    autocomplete_fields = [
        "item",
        "event_type",
        "model_version",
        "labels",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "item",
                        "model_version",
                    ),
                    ("event_type", "annotation_type", "certainty"),
                    (
                        "annotation",
                        "labels",
                    ),
                )
            },
        ),
    )
