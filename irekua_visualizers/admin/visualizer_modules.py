from irekua_database.admin.base import IrekuaAdmin


class VisualizerModuleAdmin(IrekuaAdmin):
    search_fields = [
        "visualizer_version__visualizer__name",
        "visualizer_version__version",
    ]

    list_display = (
        "id",
        "__str__",
        "visualizer_version",
        "is_active",
        "created_on",
    )

    list_display_links = (
        "id",
        "__str__",
    )

    list_filter = ("is_active",)

    fieldsets = (
        (
            None,
            {"fields": ("visualizer_version", "javascript_file", "is_active")},
        ),
    )
