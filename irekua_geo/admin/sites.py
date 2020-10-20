from django.utils.translation import gettext_lazy as _

from irekua_database.admin.base import IrekuaUserAdmin


class SiteAdmin(IrekuaUserAdmin):
    search_fields = [
        'name',
        'locality__name',
    ]

    list_display = [
        'id',
        'name',
        'locality',
        'latitude',
        'longitude',
        'altitude',
        'created_on',
    ]

    list_display_links = [
        'id',
        'name',
    ]

    list_filter = [
        'latitude',
        'longitude',
        'created_on',
    ]

    autocomplete_fields = [
        'locality',
    ]

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'locality'),
            )
        }),
        (_('Position'), {
            'fields': (
                ('geo_ref', ),
                ('longitude', 'latitude', 'altitude'),
            )
        })
    )
