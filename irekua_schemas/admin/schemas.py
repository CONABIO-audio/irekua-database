from irekua_database.admin.base import IrekuaAdmin


class SchemaAdmin(IrekuaAdmin):
    search_fields = [
        'name',
    ]

    list_display = [
        'id',
        'name',
        'created_on',
    ]

    list_display_links = [
        'id',
        'name',
    ]

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                'schema',
            )
        }),
    )
