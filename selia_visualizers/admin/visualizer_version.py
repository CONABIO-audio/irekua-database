from django.contrib import admin


class VisualizerVersionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = ['visualizer__name', 'version']
    list_display = (
        'id',
        'visualizer',
        'version',
        'created_on',
    )
    readonly_fields = ('created_on',)
    list_display_links = ('id', 'visualizer', 'version')
    list_filter = (
        'visualizer',
        'version',
        'created_on',
    )

    fieldsets = (
        (None, {
            'fields': (
                ('visualizer', 'version'),
                ('created_on',),
            )
        }),
        ('Configuration', {
            'classes': ('collapse',),
            'fields': ('configuration_schema',),
        }),
    )
