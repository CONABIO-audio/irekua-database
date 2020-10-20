from irekua_database.admin.base import IrekuaAdmin


class DeviceBrandAdmin(IrekuaAdmin):
    search_fields = [
        'name',
    ]

    list_display = [
        'id',
        'name',
        'website',
        'created_on',
    ]

    list_display_links = [
        'id',
        'name'
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'website'),
                'logo',
            )
        }),
    )
