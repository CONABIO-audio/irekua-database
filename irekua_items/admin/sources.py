from irekua_database.admin.base import IrekuaAdmin


class SourceAdmin(IrekuaAdmin):
    search_fields = [
        'directory',
        'parse_function',
    ]

    list_display = [
        'id',
        'directory',
        'parse_function',
        'uploader',
        'created_on',
    ]

    list_display_links = [
        'id',
        'directory',
    ]

    autocomplete_fields = [
        'uploader',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('directory', 'source_file'),
                ('parse_function', 'uploader')
            )
        }),
    )
