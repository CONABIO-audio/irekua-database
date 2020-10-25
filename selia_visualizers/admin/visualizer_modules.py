from irekua_database.admin.base import IrekuaAdmin


class VisualizerModuleAdmin(IrekuaAdmin):
    search_fields = [
        'visualizer__name',
        'version',
    ]

    list_display = (
        'id',
        '__str__',
        'visualizer',
        'version',
        'is_active',
        'created_on',
    )

    list_display_links = (
        'id',
        '__str__',
    )

    list_filter = (
        'visualizer',
        'version',
        'created_on',
        'is_active',
    )

    fieldsets = (
        (None, {
            'fields': (
                ('visualizer', 'version'),
                'javascript_file',
                'is_active'
            )
        }),
        ('Configuration', {
            'fields': ('configuration_schema',),
        }),
    )
