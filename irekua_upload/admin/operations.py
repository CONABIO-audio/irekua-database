from irekua_database.admin.base import IrekuaAdmin


class OperationAdmin(IrekuaAdmin):
    search_fields = [
        'name'
    ]

    list_display = [
        'id',
        '__str__',
        'created_on',
    ]

    list_display_links = [
        'id',
        '__str__',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'python_file'),
                'description',
            )
        }),
    )
