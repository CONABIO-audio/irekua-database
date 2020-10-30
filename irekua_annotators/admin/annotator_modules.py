from irekua_database.admin.base import IrekuaAdmin


class AnnotatorModuleAdmin(IrekuaAdmin):
    date_hierarchy = 'created_on'

    search_fields = [
        'annotator_version__annotator__name',
        'annotator_version__version',
    ]

    list_display = [
        'id',
        '__str__',
        'annotator_version',
        'is_active',
        'created_on',
    ]

    list_display_links = [
        'id',
        '__str__',
    ]

    autocomplete_fields = [
        'annotator_version',
    ]

    list_filter = [
        'annotator_version__annotator',
    ]

    fieldsets = (
        (None, {
            'fields': (
                'annotator_version',
                'javascript_file',
                'is_active',
            )
        }),
    )
