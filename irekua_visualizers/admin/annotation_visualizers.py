from irekua_database.admin.base import IrekuaAdmin


class AnnotationVisualizerAdmin(IrekuaAdmin):
    search_fields = [
        'annotation__id',
        'visualizer_version__visualizer__name',
        'visualizer_version__version',
    ]

    list_display = (
        'id',
        'annotation',
        'visualizer_version',
        'created_on',
    )

    list_display_links = (
        'id',
        'annotation',
    )

    list_filter = (
        'annotation__annotation_type',
        'visualizer_version__visualizer',
    )

    autocomplete_fields = [
        'annotation',
        'visualizer_version',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('visualizer_version', 'annotation'),
                'visualizer_configuration',
            )
        }),
    )
